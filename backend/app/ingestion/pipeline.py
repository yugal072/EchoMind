from pathlib import Path
from typing import List, Dict, Optional
from langchain_core.documents import Document
from bs4 import BeautifulSoup
import uuid
import hashlib
from datetime import datetime
from email.utils import parsedate_to_datetime

from app.ingestion.parsers.email_parser import parse_emails, clean_html
from app.ingestion.parsers.llama_parser import parse_pdfs
from app.ingestion.connectors.audio import load_audio_file
from app.ingestion.connectors.sms import get_sms_to_documents

from app.ingestion.connectors.calendar import list_upcomming_events
from app.ingestion.parsers.calender_parser import parse_events

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import VECTORSTORE_DIR, DUMPS_DIR


def clean_email_body(html_content: str) -> str:
    """Convert HTML email to clean plain text"""
    # Option A: BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return text


def load_email_documents(max_results=20) -> list[Document]:
    docs = []
    for e in parse_emails(max_results):
        text = f"Subject: {e['subject']}\nFrom:{e['from']}\nDate:{e['date']}\nText:{clean_email_body(e['text'])}"

        try:
            date_ts = parsedate_to_datetime(e["date"]).timestamp() if e.get("date") else None
        except Exception:
            date_ts = None

        docs.append(Document(page_content=text, metadata={
            "source": "gmail",
            "id": e["id"],
            "subject": e["subject"],
            "from": e["from"],
            "sender": e["from"],
            "date": e["date"],
            "date_ts": date_ts,
            "ingested_at": datetime.now().isoformat(),
            "document_type": "email",
        }))
    return docs

def load_calendar_documents():
    """Load calendar events and convert them to langchain Documents"""
    raw_events = list_upcomming_events(max_result=20)
    documents = parse_events(raw_events)
    return documents

def get_calendar_ids(chunks):
    """Generate unique ids for calendar chunks to prevent duplicates"""
    ids=[]
    for i, chunk in enumerate(chunks):
        event_id = chunk.metadata.get("event_id",f"unknown_{i}")
        filename = Path(event_id).name
        custom_id= f"calendar_{filename}_chunk[i]"
        uuid_id= generate_uuid_from_string(custom_id)
        ids.append(uuid_id)
    return ids
     

def generate_uuid_from_string(text:str) ->str:
    """Generate a consistent UUID from any string"""
    # Use UUID5 (SHA1-based) with a fixed namespace for consistency
    return str(uuid.uuid5(uuid.NAMESPACE_URL, text))
     
def get_email_ids(chunks):
    ids = []
    for chunk in chunks:
        email_id = chunk.metadata.get("id")
        custom_id = f"email_{email_id}"
        uuid_id = generate_uuid_from_string(custom_id)
        
        ids.append(uuid_id)
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
                    "subject": path.stem,                     # stem (no extension) is the human-readable title
                    "path": str(path),
                    "ingested_at": datetime.now().isoformat(),
                    "date_ts": path.stat().st_mtime,          # file's last-modified time as a Unix timestamp
                    "file_size": len(content),
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
    parsed_data= parse_pdfs()
    for item in parsed_data:
        try:
            text = item.get("text","").strip()
            if not text:
                continue  # skip empty doc
            
            llama_meta = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
            
            flat_meta = {
                        "source": "pdf",
                        "document_type": "pdf",
                        "filename": llama_meta.get("file_name") or llama_meta.get("name") or "unknown.pdf",
                        "subject": llama_meta.get("title") or llama_meta.get("file_name") or llama_meta.get("name") or "unknown.pdf",
                        "ingested_at": datetime.now().isoformat(),
                        "date_ts": datetime.now().timestamp(),  # PDFs rarely have a reliable creation date; use ingestion time
                        "page_count": llama_meta.get("total_pages", 1),
                        "file_size": len(text),
                        }
           
            # add other useful metadata if available
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
            
    print(f"✅ Loaded {len(docs)} PDF documents into LangChain format")

    return docs

def get_pdf_ids(chunks):
    ids = []
    for i, chunk in enumerate(chunks):
        # Use 'filename' (e.g. "mybook.pdf") not 'source' (the literal string "pdf")
        filename = chunk.metadata.get("filename", "unknown.pdf")
        filename = Path(filename).name
        custom_id = f"pdf_{filename}_chunk{i}"
        uuid_id = generate_uuid_from_string(custom_id)
        ids.append(uuid_id)
    return ids

def get_file_ids(chunks):
    ids = []
    for i, chunk in enumerate(chunks):
        # Use 'filename' (e.g. "notes.txt") not 'source' (the literal string "file")
        filename = chunk.metadata.get("filename", "unknown")
        filename = Path(filename).name
        custom_id = f"txt_{filename}_chunk{i}"
        uuid_id = generate_uuid_from_string(custom_id)
        ids.append(uuid_id)
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