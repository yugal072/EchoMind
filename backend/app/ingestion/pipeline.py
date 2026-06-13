from pathlib import Path
from langchain_core.documents import Document
from bs4 import BeautifulSoup

from app.ingestion.parsers.email_parser import parse_emails, clean_html
from app.ingestion.parsers.llama_parser import parse_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.core.config import VECTORSTORE_DIR, DUMPS_DIR


def clean_email_body(html_content: str) -> str:
    """Convert HTML email to clean plain text"""
    # Option A: BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return text


def load_email_documents(max_results=20)->list[Document]: 
    docs = []
    for e in parse_emails(max_results):
        text = f"Subject: {e['subject']}\nFrom:{e['from']}\nDate:{e['date']}\nText:{clean_email_body(e['text'])}"
        docs.append(Document(page_content= text, metadata={"source":"gmail",
                                                           "id":e["id"],
                                                           "subject":e["subject"],
                                                           "from":e["from"],
                                                           "date":e["date"]}
                             ))
    return docs

def load_file_documents()->list[Document]:
    docs=[]
    for path in DUMPS_DIR.glob("*.txt"):
        docs.append(Document(page_content=path.read_text(),
                             metadata={"source":"file", "path":str(path)}
                             )
                    )
    return docs

def load_pdf_documents() -> list[Document]:
    docs = []
    for e in parse_pdfs():
        flat_meta = {"source": "pdf"}
        llama_meta = e.get("metadata")
        if isinstance(llama_meta, dict):
            for key, val in llama_meta.items():
                if isinstance(val, (str, int, float, bool)) or val is None:
                    flat_meta[key] = val
        docs.append(Document(page_content=e["text"], metadata=flat_meta))
    return docs

def run_ingestion()->list[Document]:
    all_docs = []
    all_docs.extend(load_file_documents())
    email_docs = load_email_documents()
    print("Emails:", len(email_docs))

    pdf_docs = load_pdf_documents()
    print("PDFs:", len(pdf_docs))
    
    all_docs.extend(email_docs)
    all_docs.extend(pdf_docs)
    
    return all_docs

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap=80)
    chunks = text_splitter.split_documents(documents=documents)
    return chunks