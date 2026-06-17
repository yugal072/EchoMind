from io import BytesIO
from datetime import datetime
from langchain_core.documents import Document
from pypdf import PdfReader

def parse_uploaded_pdfs(upload_file):
    pdf_bytes = upload_file.file.read()
    
    pdf = PdfReader(BytesIO(pdf_bytes))
    
    text = ""
    
    for page in pdf.pages:
         text += page.extract_text() or ""
         
    doc = Document(
        page_content = text,
        metadata= {
            "source":"upload",
            "document_type":"pdf",
            "filename": upload_file.filename,
            "ingested_at":datetime.now().isoformat()
        }
    )
    return [doc]


def parse_uploaded_txt(upload_file):
    content = upload_file.file.read().decode("utf-8")
    
    doc = Document(
        page_content=content,
        metadata={
            "source":"upload",
            "document_type":"TXT",
            "filename":upload_file.filename,
            "ingested_at":datetime.now().isoformat()
        }
    )
    return [doc]


def parse_uploaded_file(upload_file):
    filename = upload_file.filename.lower()
    print("File: ",filename)
    if filename.endswith(".pdf"):
        print("PDF Detected")
        return parse_uploaded_pdfs(upload_file)
    
    if filename.endswith(".txt"):
        print("TXT Detected")
        return parse_uploaded_txt(upload_file)
    
    raise ValueError(
        f"Unsupported file type: {filename}"
    )