import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict
load_dotenv()
import json, re

from app.core.config import VECTORSTORE_DIR
from app.RAG.metadatas.filters import build_metadata_filter
from app.sessions.session_store import PersistentSessionStore, PersistentChatMessageHistory
from app.RAG.metadatas.qdrant_translator import to_qdrant_filter

BASE = Path(__file__).resolve().parents[2]
STORE_PATH = str(VECTORSTORE_DIR)


from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models 
from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

embeddings = OllamaEmbeddings(model="nomic-embed-text")

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", api_key= os.getenv("GROQ_API_KEY"))

_vectorstore = None

system_prompt = (
    """ 
    You are EchoMind, a precise and trustworthy personal knowledge assistant.
    
    **Core Rules:**
    - Answer **only** using information present in the provided context.
    - Extract **exact** details like URLs, dates, names, deadlines when the user asks for them.
    - Be **direct, concise, and accurate**. Avoid unnecessary explanations.
    - If the context does not contain the answer, reply exactly: "I don't have enough information in my knowledge base to answer this."
    - Do NOT hallucinate names, dates, emails, or any facts.
    - Do NOT add extra explanations, suggestions, or commentary unless specifically asked.
    - Do NOT say "Based on the context" or "According to the documents" in the final answer.

    **Knowledge Base Sources:**
    Your context may come from five different sources, each with its own relevant details to surface:
    - gmail     → emails: mention sender and subject when relevant
    - pdf       → documents: mention document/file name when relevant
    - audio     → voice note transcriptions: mention that it's a voice note and its language if relevant
    - calendar  → events: mention event time, location, and attendee count when relevant
    - obsidian  → personal notes: mention note title, tags, or folder when relevant

    **Advanced Capability - Smart Filtering:**
    You can understand natural language requests that imply filters.
    When the user mentions dates, senders, subjects, tags, folders, or document types,
    intelligently extract and focus on the most relevant documents from the context.

    Examples of user intent:
    - "emails from placement" → focus on source=gmail and sender containing "placement"
    - "last email about internship" → look for recent emails with "internship" in subject or body
    - "What happened on 10/06/2026" → prioritize documents with date around 10 June 2026
    - "PDFs about project X" → focus on source=pdf and subject/filename containing "project X"
    - "meetings today" → focus on source=calendar with date matching today
    - "notes tagged research" → focus on source=obsidian with tags containing "research"
    - "voice notes about the trip" → focus on source=audio and subject/transcript mentioning "trip"

    **Response Style:**
    - Be natural and professional.
    - Prioritize the most relevant information.
    - Use bullet points only when it improves readability.
    - Stay strictly relevant to what the user asked.
        
    <context>
    {context}
    </context>
    """
)


def get_vectorstore():
    """Connect to the Qdrant server and return (or reuse) the vectorstore."""
    global _vectorstore

    if _vectorstore is None:
        # Read connection details from .env (QDRANT_HOST / QDRANT_PORT).
        # Falls back to localhost:6333 if the vars are absent.
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "echomind_documents")

        client = QdrantClient(url=f"http://{qdrant_host}:{qdrant_port}")

        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE,
                ),
            )
            print(f"✅ Created new Qdrant collection: {collection_name}")
        else:
            print(f"✅ Using existing Qdrant collection: {collection_name}")

        # Create (or re-create) payload text indexes every startup.
        # On a real Qdrant server this is idempotent — safe to call even if
        # the index already exists. This was previously inside the
        # "new collection only" branch, which meant server restarts silently
        # lost the indexes.  MatchText filters require these indexes to work.
        TEXT_INDEX_FIELDS = ("metadata.sender", "metadata.subject", "metadata.summary", 
                     "metadata.note_title", "metadata.location")
        for field in TEXT_INDEX_FIELDS:
            try:
                client.create_payload_index(
                    collection_name=collection_name,
                    field_name=field,
                    field_schema=models.TextIndexParams(
                        type="text", tokenizer=models.TokenizerType.WORD, min_token_len=2, lowercase=True,
                    ),
                )
            except Exception as idx_err:
                print(f"⚠️ Payload index for '{field}': {idx_err}")

        _vectorstore = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )
    return _vectorstore
    
    
def get_retriever(
                  k:int =6,
                  score_threshold: float=0.05,
                  metadata_filter: Optional[Dict]= None):
    vectorstore = get_vectorstore()
    print(f"DEBUG - Applying filter: {metadata_filter}")   # Important debug
    
    search_kwargs ={"k": k, "filter": metadata_filter} if metadata_filter else {"k": k}
    
    if metadata_filter:
        search_kwargs["filter"] = metadata_filter
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )
    return retriever



def get_session_history(session_id:str):
    return PersistentChatMessageHistory(session_id=session_id)

# Contextual Promppt to reframe the context based on the previous and present questions and responses

contextual_prompt = ChatPromptTemplate.from_messages([
    ('system', 
     "Given the chat history and the latest user question, rephrase the question into a "
     "standalone version that can be understood without the chat history. "
     "Do NOT answer the question. Do NOT explain or add information. "
     "Output ONLY the rephrased question itself, as a single sentence, with no preamble, "
     "no headers, no bullet points, no extra commentary. "
     "If the question is already standalone, return it unchanged."),
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

    
VALID_FILTER_KEYS = {"source", "sender", "subject", "date_after", "date_before", "document_type"}

def get_rag_chain(filter_dict: Optional[Dict] = None):
    vectorstore = get_vectorstore()
    print(f"DEBUG - Raw filter_dict received: {filter_dict}")

    EXACT_FILTER_KEYS = {"source", "sender", "subject", "document_type", "tags", "folder", "language", "location"}
    DATE_FILTER_KEYS  = {"date_after", "date_before"}

    clean_kwargs = {}

    if filter_dict:
        for k, v in filter_dict.items():
            if isinstance(v, tuple) and len(v) == 1:
                v = v[0]
            if v is None:
                continue
            cleaned = str(v).strip()
            if not cleaned or cleaned.lower() in ["none", "null", "", "()", "(none,)"]:
                continue
            if k in EXACT_FILTER_KEYS or k in DATE_FILTER_KEYS:
                clean_kwargs[k] = cleaned

    print(f"DEBUG - Cleaned kwargs: {clean_kwargs}")

    filter_spec = build_metadata_filter(**clean_kwargs) if clean_kwargs else None
    qdrant_filter = to_qdrant_filter(filter_spec)
    print(f"DEBUG - Final Qdrant filter: {qdrant_filter}")

    retriever = get_retriever(
        metadata_filter=qdrant_filter,
        k=8,
        score_threshold=0.05,
    )

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextual_prompt)
    document_chain  = create_stuff_documents_chain(llm=llm, prompt=final_prompt)
    retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain


filter_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a SMART FILTER EXTRACTION BOT.

YOUR ONLY JOB IS TO RETURN A VALID JSON OBJECT. NOTHING ELSE. NO EXPLANATIONS.

The knowledge base contains FIVE types of documents:
- "gmail"    → emails (fields: sender, subject, date)
- "pdf"      → PDF documents (fields: subject/filename, date)
- "audio"    → voice note transcriptions (fields: subject/filename, language, date)
- "calendar" → calendar events (fields: subject/summary, location, date)
- "obsidian" → personal notes (fields: subject/note_title, tags, folder, date)

Rules:
- If the question is a **general knowledge question** that doesn't target a specific document type
  (e.g. "who is the author", "what is the book about", "summarize", "explain X"), return exactly: {{}}
- Only return filters if the user is clearly asking about **specific documents**.
- Valid keys: "source", "sender", "subject", "date_after", "date_before", "tags", "folder", "language", "location"
- "source" can only be one of: "gmail", "pdf", "audio", "calendar", "obsidian"
- "tags" should be a comma-separated string if multiple tags are implied (e.g. "internship,placement")
- "date_after"/"date_before" can be relative ("recent", "today", "last week") or absolute (DD/MM/YYYY)
- Only include keys that are clearly implied — do not guess fields that aren't mentioned

Examples:

User: "emails from placement?"
Output: {{"source": "gmail", "subject": "placement"}}

User: "Show me emails from placement cell"
Output: {{"source": "gmail", "sender": "placement"}}

User: "What meetings do I have today"
Output: {{"source": "calendar", "date_after": "today", "date_before": "today"}}

User: "Find my notes tagged internship"
Output: {{"source": "obsidian", "tags": "internship"}}

User: "Notes in my Research folder about LLMs"
Output: {{"source": "obsidian", "folder": "Research", "subject": "LLMs"}}

User: "Any voice notes in Hindi about the project"
Output: {{"source": "audio", "language": "hindi", "subject": "project"}}

User: "Where is my meeting with the PACCAR recruiter"
Output: {{"source": "calendar", "subject": "PACCAR recruiter"}}

User: "Who is the author of Thinking Fast and Slow?"
Output: {{"source": "pdf", "subject": "Thinking Fast and Slow"}}

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