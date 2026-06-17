import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict
load_dotenv()

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
                  score_threshold: float=0.1,
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
    
VALID_FILTER_KEYS = {"source", "sender", "subject", "date_after", "date_before", "document_type"}

def get_rag_chain(**filter_kwargs):
    vectorstore = get_vectorstore()
    clean_kwargs = {}
    for k, v in filter_kwargs.items():
        if k not in VALID_FILTER_KEYS:
            continue
        if v is not None:
            cleaned = str(v).strip()
            if cleaned and cleaned.lower() not in ["none", "null", "()", "(none,)"]:
                clean_kwargs[k] = cleaned
    
    print(f"DEBUG - Cleaned kwargs: {clean_kwargs}")
    
    metadata_filter = build_metadata_filter(**clean_kwargs) if clean_kwargs else None          # creating filters from filters.py only when parameters are given
    print(f"DEBUG - Final filter: {metadata_filter}")
    
    retriever = get_retriever(vectorstore=vectorstore, 
                              metadata_filter=metadata_filter,
                              k=6
                              )
    
    history_aware_retriever = create_history_aware_retriever(llm,retriever, contextual_prompt)
    
    document_chain = create_stuff_documents_chain(llm=llm, prompt = final_prompt)
    retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
    
    conversational_rag_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    return conversational_rag_chain



filter_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at extracting search filters from user questions.

Extract the following filters if mentioned:
- source: "gmail", "pdf", or "file"
- sender: email address or name
- subject: keyword from subject
- date_after: date in YYYY-MM-DD format
- date_before: date in YYYY-MM-DD format

Return ONLY a valid JSON object. If nothing is mentioned, return empty object.

Example:
User: "Show me placement emails from last week"
Output: {{"source": "gmail", "subject": "placement"}}

User: "What emails did I receive on 10/06/2026?"
Output: {{"source": "gmail", "date_after": "2026-06-10", "date_before": "2026-06-10"}}
"""),
    ("human", "{input}")
])


def extract_filters(question: str) -> Dict:
    chain = filter_extraction_prompt | llm
    response = chain.invoke({"input": question})
    
    try:
        import json
        filters = json.loads(response.content)
        print(f"Extracted filters: {filters}")   # Debug
        return filters
    except:
        print("Failed to parse filters, using no filter")
        return {}
    
    
    
def ask(question:str, session_id:str = "default", **filter_kwargs):
    print(f"Question: {question}")
    extracted_filters = extract_filters(question)
    print(f"Extraced filters: {extracted_filters}")
    
    final_filters = {**extracted_filters, **filter_kwargs}
    
    chain = get_rag_chain(**final_filters)
    response = chain.invoke({'input': question}, config={'configurable':{'session_id':session_id}})
    
    context = [
        doc.page_content
        for doc in response.get('context',[])
    ]
    return {
        'answer': response['answer'],
        'sources': [doc.metadata for doc in response.get('context', [])],
        'context':context
    }
    
    
# For testing 
if __name__ == "__main__":
    result = ask(question="What email did i receive from placement cell?",)
    print("Answer:", result['answer'])
    print("context:", result['context'])
    print("\nNumber of sources:", len(result['sources']))