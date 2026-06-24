from pathlib import Path
from typing import List, Dict, Optional
from langchain_core.documents import Document
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime

from app.ingestion.parsers.email_parser import parse_emails, clean_html
from app.ingestion.parsers.llama_parser import parse_pdfs
from app.ingestion.connectors.audio import load_audio_file
from app.ingestion.connectors.sms import get_sms_to_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
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
                                                           "date":e["date"],
                                                           "ingested_at": datetime.now().isoformat(),
                                                           "document_type":"email"}
                             ))
    return docs

def get_email_ids(chunks):
    ids = []
    for chunk in chunks:
        email_id = chunk.metadata.get("id")
        if email_id:
            # Best: Use original Gmail ID + short hash of content
            content_hash = hashlib.md5(chunk.page_content[:500].encode('utf-8')).hexdigest()[:8]
            doc_id = f"email_{email_id}_{content_hash}"
        else:
            # Fallback
            doc_id = f"email_unknown_{hashlib.md5(chunk.page_content[:200].encode('utf-8')).hexdigest()[:12]}"
        
        ids.append(doc_id)
    return ids

def load_sms_documents(sms_data:List[Dict]):
    documents = get_sms_to_documents(sms_data)
    return documents



def load_audio_documents(
    audio_dir: Optional[str] = None,
    uploaded_file_path: Optional[str] = None,
    audio_files: Optional[List[str]] = None
    
) -> List[Document]:
    
    documents = []
    
    # Priority: UI Upload > List of files > Directory
    if uploaded_file_path:
        try:
            docs = load_audio_file(uploaded_file_path)
            documents.extend(docs)
            print(f"✅ Transcribed uploaded file: {Path(uploaded_file_path).name}")
        except Exception as e:
            print(f"❌ Failed uploaded file {uploaded_file_path}: {e}")
            
    elif audio_files:
        for path in audio_files:
            try:
                docs = load_audio_file(path)
                documents.extend(docs)
            except Exception as e:
                print(f"❌ Failed {path}: {e}")
                
    elif audio_dir:
        # Your existing folder logic here...
        pass
    
    return documents

def generate_audio_ids(chunks):
    return [f"audio_{chunk.metadata['filename']}_{i}" for i, chunk in enumerate(chunks)]
    
def load_file_documents()->list[Document]:
    docs=[]
    for path in DUMPS_DIR.glob("*.txt"):
        try:
            content = path.read_text(encoding="utf-8")
            
            doc = Document(
                page_content=content,
                metadata={
                    "source": "file",
                    "document_type": "text",
                    "filename": path.name,
                    "path": str(path),
                    "ingested_at": datetime.now().isoformat(),
                    "file_size": len(content),                    # useful for debugging
                    "extension": ".txt",
                }
            )
            docs.append(doc)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            continue
    return docs

def load_pdf_documents() -> list[Document]:
    docs = []
    for e in parse_pdfs():
        try:
            text = e.get("text","")
            llama_meta = e.get("metadata", {}) if isinstance(e.get("metadata"), dict) else {}
            
            flat_meta = {"source": "pdf",
                         "document_type":"pdf",
                         "filename":llama_meta.get("file_name") or llama_meta.get("name") or "unknown.pdf",
                         "ingested_at":datetime.now().isoformat(),
                         "page_count":llama_meta.get("total_pages", 1),
                         "file_size":len(text)
                         }
           
            for key in ["title", "author", "creation_date", "mod_date", "page_number"]:
                if key in llama_meta and llama_meta[key]:
                    flat_meta[key] = llama_meta[key]
            
            doc = Document(
                page_content=text,
                metadata=flat_meta
            )
            docs.append(doc)
            
        except Exception as e:
            print(f"Error processing PDF document: {e}")
            continue
            
    return docs

def get_pdf_ids(chunks):
    ids = []
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown.pdf")
        filename = Path(source).name
        content_hash = hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()[:12]
        doc_id = f"pdf_{filename}_{content_hash}"
        ids.append(doc_id)
    return ids

def get_file_ids(chunks):
    ids = []
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown.txt")
        filename = Path(source).name
        content_hash = hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()[:12]
        doc_id = f"file_{filename}_{content_hash}"
        ids.append(doc_id)
    return ids

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