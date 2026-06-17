from app.ingestion.pipeline import split_documents
from app.RAG.index import get_vectorstore
import hashlib
import re

def generate_ids(chunks, prefix="upload"):
    ids=[]
    
    for idx,chunk in enumerate(chunks):
        filename = chunk.metadata.get("filename","unknown")
        filename = re.sub(
            r"[^a-zA-Z0-9_-]",      # sanitize filename
            "_",
            filename
        )
        
        content_hash =  hashlib.md5(chunk.page_content.encode('utf-8')).hexdigest()[:12]
        
        doc_id = (
            f"{prefix}_"
            f"{filename}_"              ## no comma 
            f"{idx}_"
            f"{content_hash}"
        )
        ids.append(doc_id)
        
    return ids


def ingest_documents(documents, prefix= "upload"):
    chunks = split_documents(documents)
    print("CHUNKS:", len(chunks))
    
    ids = generate_ids(chunks, prefix)
    
    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents=chunks,
                              ids = ids)
    return len(chunks)