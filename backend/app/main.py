from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, UploadFile, File

from fastapi.responses import JSONResponse
import logging
import os.path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from pathlib import Path

from app.RAG.index import ask
from app.ingestion.ingest import build_index
from app.ingestion.pipeline import generate_uuid_from_string
from app.RAG.metadatas.filters import build_metadata_filter


from app.ingestion.connectors.obsidian import ingest_obsidian_vault
from app.ingestion.loaders.upload_loader import parse_uploaded_file
from app.ingestion.pipeline import generate_audio_ids, load_audio_documents
from app.RAG.index import get_vectorstore
from app.ingestion.loaders.vector_ingestion import ingest_documents
from app.ingestion.connectors.sms import get_sms_to_documents
from app.ingestion.pipeline import split_documents

#setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EchoMind", description="API for EchoMind RAG system", version="1.0")

@app.exception_handler(Exception)
async def global_exception_handler(request:Request, exc:Exception):
    logger.error(f"An unexpected error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "details": str(exc)},
    )
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
    
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=600, description="The question to ask the RAG system.")
    session_id: str = Field(..., min_length=1, max_length=100)
    source: Optional[str] = None
    sender: Optional[str] = None
    subject: Optional[str] = None
    date_after: Optional[str] = None
    date_before: Optional[str] = None
    document_type: Optional[str] = None
    # Extended filter fields — supported by build_metadata_filter() and the LLM extraction prompt
    tags: Optional[str] = None        # comma-separated tag string, e.g. "internship,placement"
    folder: Optional[str] = None      # obsidian folder name
    language: Optional[str] = None    # audio transcription language
    location: Optional[str] = None    # calendar event location
    
class AudioIngestRequest(BaseModel):
    file_path: str
    
class SMSIngestionRequest(BaseModel):
    sms_messages: List[Dict]
    device: Optional[str] = "andriod"
    api_key: Optional[str] = None
    
class ObsidianIngestRequest(BaseModel):
    folder_path:str
    subfolders: Optional[List[str]] = None    # optional 

@app.post("/upload")
async def upload_files(files: list[UploadFile]= File(...)):
    try:
        total_chunks=0
        for file in files:
            
            documents = parse_uploaded_file(file)
            print(len(documents))
            print(documents[0].metadata)
            
            chunk_count = ingest_documents(documents, prefix="upload") # the function is of ingest documents but it returns number of chunks
            vectorstore= get_vectorstore()
            
            print("TOTAL DOCS:", vectorstore._collection.count())
            total_chunks+=chunk_count
            
        return {
            "status":"success",
            "filename":file.filename,
            "chunks_added": total_chunks
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )    


@app.post("/ingest")
async def ingest_data(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(build_index)
        
        return{
            "status":"success",
            "message":"Ingestion process has started in the background. You will be notified once it's complete.",
            "detail":"check/ingest/status for progress updates."
            
        }
    except Exception as e:
        logger.error(f"Error during ingestion: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during ingestion.")
    



@app.post("/ingest/sms")
async def ingest_sms(payload: SMSIngestionRequest):
    try:
        if payload.api_key and payload.api_key != "echo_mind_sms_2026_x7k9m2p9v4q8":
            raise HTTPException(status_code=403, detail="Invalid API key")
        
        if not payload.sms_messages:
            return {"status": "success", "message": "No SMS received"}
        
        documents = get_sms_to_documents(payload.sms_messages)
        if not documents:
            return {"status": "warning", "message": "No valid SMS parsed"}
        
        chunks = split_documents(documents)
        sms_ids = [f"sms_{chunk.metadata.get('message_id', i)}_{i}" 
                   for i, chunk in enumerate(chunks)]
        
        vectorstore = get_vectorstore()
        vectorstore.add_documents(documents=chunks, ids = sms_ids)
        
        total_chunks = len(chunks)
        return {
            "status":"success",
            "message":f"Succcessfully ingested {len(documents)} sms messages",
            "chunks_added":total_chunks
        }
    except Exception as e:
        logger.error(f"SMS ingestion error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@app.post("/ingest/audio")
async def ingest_audio(request: AudioIngestRequest):
    try:
        print(f"Received request to ingest: {request.file_path}")
        documents = load_audio_documents(uploaded_file_path = request.file_path)
        if not documents:
            raise HTTPException(status_code=400, detail="No documents created from audio")
        
        chunks = split_documents(documents)
        
        vectorstore= get_vectorstore()
        vectorstore.add_documents(documents=chunks, ids= generate_audio_ids(chunks))
        
        return {
            "status": "success", 
            "message": f"Added {len(chunks)} audio chunks",
            "filename": Path(request.file_path).name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.post("/ingest/obsidian")
async def ingest_obsidian(request: ObsidianIngestRequest):
    try: 
        if not request.folder_path or not os.path.isdir(request.folder_path):
            raise HTTPException(status_code=400, detail="Invalid vault path")
        
        documents = ingest_obsidian_vault(
            vault_path=request.folder_path,
            subfolders=request.subfolders
        )
        
        ids = [
            generate_uuid_from_string(f"obsidian_{doc.metadata.get('file_path', i)}")
            for i, doc in enumerate(documents)
        ]
        
        # Add to vectorstore
        vectorstore = get_vectorstore()
        vectorstore.add_documents(documents)
        
        return {
            "status" : "success",
            "message": f"Successfully ingested {len(documents)} documents from obsidian vault",
            "chunks_added": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
        result = ask(
            question=request.question,
            session_id=request.session_id,
            source=request.source,
            sender=request.sender,
            subject=request.subject,
            date_after=request.date_after,
            date_before=request.date_before,
            document_type=request.document_type,
            tags=request.tags,
            folder=request.folder,
            language=request.language,
            location=request.location,
        )
        return {"answer": result["answer"], "sources": result["sources"], "session_id": request.session_id, "token_usage": result['token_usage']} #, "output_tokens": result['output_tokens'], "total_tokens":result['total_tokens']}
    except HTTPException:
        raise # auto handled by FastAPI
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

