import os
import sys
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

BASE = Path(__file__).resolve().parents[3]
DUMPS = BASE/ "data"/"files"/"dumps"
STORE = BASE/ "data"/"vectorstore"
persist_directory = str(STORE)

APP_DIR =  Path(__file__).resolve().parents[2]
INGESTION_DIR = APP_DIR/"ingestion"

for p in (APP_DIR, INGESTION_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from ingestion.pipeline import run_ingestion, split_documents

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq
from langchain_classic.prompts import PromptTemplate, ChatPromptTemplate


embeddings = NVIDIAEmbeddings()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)

prompt = ChatPromptTemplate.from_template(
    """
    Analyse the emails and pdfs and answer the query based on the given context only.
    Provide the most accurate response based on the requirements and questions asked.
    <context>
    {context}
    </context>
    Questions: {input}
    """
)

# This program reingest and remake the database everytime it runs. So whe need to make a new script 
# independent of it so that it can run without intervention with the old db or stores

def make_retrieval_chain(llm, embeddings):
    documents = run_ingestion()
    chunks = split_documents(documents)
    
    vectorstore = Chroma.from_documents(chunks,embeddings,persist_directory=persist_directory)
    retriever= vectorstore.as_retriever()    

    documents_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    
    retriever_chain = create_retrieval_chain(retriever, documents_chain)
    return retriever_chain


# Trial run
question= "what is the last email i got and from who?"


def invoke_retriever_chain(retriever_chain, question):
    response = retriever_chain.invoke({"input":question})
    return response



if __name__ == "__main__":
    chain = make_retrieval_chain(llm, embeddings)
    result = invoke_retriever_chain(chain, question)
    print([result['answer']])