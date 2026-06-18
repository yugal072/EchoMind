import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict
load_dotenv()
import json, re

from app.core.config import VECTORSTORE_DIR, DUMPS_DIR
from app.RAG.metadatas.filters import build_metadata_filter

BASE = Path(__file__).resolve().parents[2]
STORE_PATH = str(VECTORSTORE_DIR)

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

embeddings = NVIDIAEmbeddings()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", api_key= os.getenv("GROQ_API_KEY"))

system_prompt = (
    """ 
    You are EchoMind, a precise and trustworthy personal knowledge assistant.
    **Core Rules:**
    - Answer **only** using information present in the provided context.
    - Be **direct, concise, and accurate**. Avoid unnecessary explanations.
    - If the context does not contain enough information, reply exactly: "I don't have enough information in my knowledge base to answer this."
    - Do NOT hallucinate names, dates, emails, or any facts.
    - Do NOT say "Based on the context" or "According to the documents" in the final answer.

    **Advanced Capability - Smart Filtering:**
    You can understand natural language requests that imply filters. 
    When the user mentions dates, senders, subjects, or document types, intelligently extract and focus on the most relevant documents from the context.

    Examples of user intent:
    - "emails from placement" → focus on source=gmail and sender containing "placement"
    - "last email about internship" → look for recent emails with "internship" in subject or body
    - "What happened on 10/06/2026" → prioritize documents with date around 10 June 2026
    - "PDFs about project X" → focus on source=pdf and subject/filename containing "project X"

    **Response Style:**
    - Be helpful and natural.
    - If multiple relevant documents exist, summarize the key points clearly.
    - Use bullet points only when it improves readability.
    - Stay strictly relevant to what the user asked.
        
    <context>
    {context}
    </context>
    """
)


def get_vectorstore():
    """ Loadint the existing chroma db"""
    return Chroma(
        persist_directory=STORE_PATH,
        embedding_function=embeddings
    )
    
def get_retriever(vectorstore, 
                  k:int =6,
                  score_threshold: float=0.05,
                  metadata_filter: Optional[Dict]= None):
    
    print(f"DEBUG - Applying filter: {metadata_filter}")   # Important debug
    
    search_kwargs = {"k":k, "score_threshold":score_threshold}
    
    if metadata_filter:
        search_kwargs["filter"] = metadata_filter
    
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs=search_kwargs
    )
    return retriever



store={}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Contextual Promppt to reframe the context based on the previous and present questions and responses

contextual_prompt = ChatPromptTemplate.from_messages([
    ('system', "Rephrase the following question to be a standalone question that captures all necessary contents."),
    MessagesPlaceholder('chat_history'),
    ('human', "{input}"),
])

# Final prompt for the retrieval chain (first doc_ret_chain)

final_prompt = ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    MessagesPlaceholder('chat_history'),
    ('human', "{input}"),
])
    
    
FUZZY_DATE_VALUES = {"recent", "latest", "today", "now", "last week", "this week"}

def _resolve_date(value: str) -> Optional[str]:
    """Convert fuzzy date strings to ISO format, drop unresolvable ones."""
    from datetime import datetime, timedelta
    v = value.lower().strip()
    today = datetime.utcnow()
    
    mapping = {
        "today": today,
        "now": today,
        "recent": today - timedelta(days=7),   # treat "recent" as last 7 days
        "latest": today - timedelta(days=7),
        "last week": today - timedelta(days=7),
        "this week": today - timedelta(days=7),
    }
    if v in mapping:
        return mapping[v].strftime("%Y-%m-%d")
    
    # Try parsing as a real date
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    # Unresolvable — drop it
    print(f"⚠️ Could not resolve date value '{value}', dropping filter.")
    return None
    
    
VALID_FILTER_KEYS = {"source", "sender", "subject", "date_after", "date_before", "document_type"}

def get_rag_chain(filter_dict: Optional[Dict] = None):
    vectorstore = get_vectorstore()
    print(f"DEBUG - Raw filter_dict received: {filter_dict}")

    EXACT_FILTER_KEYS = {"source", "sender", "document_type"}
    DATE_FILTER_KEYS  = {"date_after", "date_before"}

    subject_hint = None   # goes to query augmentation, never to Chroma filter
    clean_kwargs  = {}    # only exact/range fields go here

    if filter_dict:
        for k, v in filter_dict.items():
            if isinstance(v, tuple) and len(v) == 1:
                v = v[0]
            if v is None:
                continue
            cleaned = str(v).strip()
            if not cleaned or cleaned.lower() in ["none", "null", "", "()", "(none,)"]:
                continue

            if k == "subject":
                subject_hint = cleaned          # ← extracted, NOT filtered
            elif k in EXACT_FILTER_KEYS:
                clean_kwargs[k] = cleaned
            elif k in DATE_FILTER_KEYS:
                resolved = _resolve_date(cleaned)
                if resolved:
                    clean_kwargs[k] = resolved
            # Any unrecognised key is silently dropped

    print(f"DEBUG - Chroma filter kwargs : {clean_kwargs}")
    print(f"DEBUG - Subject hint (vector): {subject_hint}")

    metadata_filter = build_metadata_filter(**clean_kwargs) if clean_kwargs else None
    print(f"DEBUG - Final filter         : {metadata_filter}")

    retriever = get_retriever(
        vectorstore=vectorstore,
        metadata_filter=metadata_filter,
        k=8,
        score_threshold=0.05,
    )

    # ── Inject subject_hint into the contextualisation prompt ──────────────
    # This steers the history-aware rephrasing step so the standalone question
    # explicitly mentions the subject keyword, improving vector recall.
    effective_contextual_prompt = contextual_prompt
    if subject_hint:
        effective_contextual_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"Rephrase the following question to be a standalone question that "
                f"captures all necessary context. Make sure the rephrased question "
                f"explicitly mentions the topic: '{subject_hint}'."
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, effective_contextual_prompt
    )
    document_chain        = create_stuff_documents_chain(llm=llm, prompt=final_prompt)
    retrieval_chain       = create_retrieval_chain(history_aware_retriever, document_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain



filter_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a FILTER EXTRACTION BOT. 

YOUR ONLY JOB IS TO RETURN A VALID JSON OBJECT. NOTHING ELSE. NO EXPLANATIONS.

Rules:
- If the question is a **general knowledge question** (like "who is the author", "what is the book about", "summarize", etc.), return exactly: {{}}
- Only return filters if the user is clearly asking for **specific documents** (emails, PDFs, files).
- Valid keys: "source", "sender", "subject", "date_after", "date_before"
- source can only be "gmail", "pdf", or "file"

Examples:

User: "What placement related emails did I receive?"
Output: {{"source": "gmail", "subject": "placement"}}

User: "Show me emails from placement cell"
Output: {{"source": "gmail", "sender": "placement"}}

User: "Who is the author of Thinking Fast and Slow?"
Output: {{"source": "pdf", "subject": "Thinking Fast and Slow}}

User: "Tell me about deliberate practice"
Output: {{"subject": "deliberate practice"}}
"""),
    ("human", "{input}")
])


def extract_filters(question: str) -> Dict:
    chain = filter_extraction_prompt | llm
    response = chain.invoke({"input": question})
    raw = response.content.strip()
    
    print(f"Raw filter response: {raw[:400]}...")

    import json, re
    
    # Try to find JSON object
    json_match = re.search(r'(\{.*?\})', raw, re.DOTALL)
    json_str = json_match.group(1) if json_match else raw

    try:
        filters = json.loads(json_str)
        if isinstance(filters, dict):
            print(f"✅ Extracted filters: {filters}")
            return filters
    except:
        pass

    print("❌ Could not parse, returning empty dict")
    return {}
    
    
    
def ask(question: str, session_id: str = "default", **filter_kwargs):
    print(f"Question: {question}")

    extracted_filters = extract_filters(question)
    print(f"Extracted filters: {extracted_filters}")
    
    explicit_filters = {
        k: v
        for k, v in filter_kwargs.items()
        if v is not None and str(v).strip() not in ["", "none", "null"]
    }

    # Merge LLM-extracted filters with any manually passed filters.
    # Manual filter_kwargs take precedence (override LLM-extracted ones).
    final_filters = {**extracted_filters, **explicit_filters}

    

    print(f"Final filters being used: {final_filters}")

    # Pass as a single dict argument, NOT as **kwargs, to avoid double-unpacking bugs
    chain = get_rag_chain(final_filters)
    response = chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )

    try:
        token_usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    except AttributeError:
        token_usage = {
            "input_tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "output_tokens": response.get("usage", {}).get("completion_tokens", 0),
            "total_tokens": response.get("usage", {}).get("total_tokens", 0),
        }

    context = [doc.page_content for doc in response.get("context", [])]
    print(f"Token Usage: {token_usage}")

    return {
        "answer": response["answer"],
        "sources": [doc.metadata for doc in response.get("context", [])],
        "context": context,
        "token_usage": token_usage,
    }    
    
        
    
# For testing 
if __name__ == "__main__":
    result = ask(question="What email did i receive from placement cell?",)
    print("Answer:", result['answer'])
    print("context:", result['context'])
    print("\nNumber of sources:", len(result['sources']))