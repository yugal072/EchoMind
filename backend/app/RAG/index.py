import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from app.core.config import VECTORSTORE_DIR, DUMPS_DIR

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
    **Strict Rules:**
    - Answer **only** using information present in the provided context.
    - Be **direct, concise, and exact**. Do not add extra explanations unless asked.
    - If the context does not contain the answer, reply exactly: "I don't have enough information in my knowledge base to answer this."
    - Do NOT make up any names, dates, emails, facts, or details.
    - Do NOT say "Based on the context" or "According to the documents" in the final answer.
    - Stay strictly relevant to the user's question. Do not add unrelated information.
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
    
def get_retriever(k:int =4):
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(
        search_type = 'similarity',
        search_kwargs = {'k':k}
    )
    
    
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
    
def get_rag_chain():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()
    
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

def ask(question:str, session_id:str = "default"):
    
    chain = get_rag_chain()
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
    result = ask("What is the last email i received regarding placement?")
    print("Answer:", result['answer'])
    print("context:", result['context'])
    print("\nNumber of sources:", len(result['sources']))