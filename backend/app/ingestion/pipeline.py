from pathlib import Path
from langchain_core.documents import Document

from parsers.email_parser import parse_emails
from parsers.llama_parser import parse_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


# paths
BASE = Path(__file__).resolve().parents[2]
DUMPS = BASE/ "data"/"files"/"dumps"
STORE = BASE/ "data"/"vectorstore"

def load_email_documents(max_results=20)->list[Document]: 
    docs = []
    for e in parse_emails(max_results):
        text = f"Subject: {e['subject']}\nFrom:{e['from']}\nDate:{e['date']}\nText:{e['text']}"
        docs.append(Document(page_content= text, metadata={"source":"gmail",
                                                           "id":e["id"],
                                                           "subject":e["subject"],
                                                           "from":e["from"],
                                                           "date":e["date"]}
                             ))
    return docs

def load_file_documents()->list[Document]:
    docs=[]
    for path in DUMPS.glob("*.txt"):
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
    all_docs.extend(load_email_documents())
    all_docs.extend(load_file_documents())
    all_docs.extend(load_pdf_documents())
    return all_docs

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap=80)
    chunks = text_splitter.split_documents(documents=documents)
    return chunks