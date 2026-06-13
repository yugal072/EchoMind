from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel, Field
from app.RAG.index import ask
from app.ingestion.ingest import build_index

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
    question: str = Field(..., min_len=1, max_len = 600, description="The question to ask the RAG system.")
    session_id: str = Field(..., min_len = 1, max_len = 100)
    
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

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
        answer, sources =  ask(request.question, session_id=request.session_id)
        return {"answer": answer, "sources": sources, "session_id": request.session_id}
    except HTTPException:
        raise # auto handled by FastAPI
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

