from fastapi import FastAPI
from pydantic import BaseModel
from app.RAG.index import ask
from app.ingestion.ingest import build_index


app = FastAPI(title="EchoMind", description="API for EchoMind RAG system", version="1.0")

class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"
    
@app.post("/ingest")
def ingest_data():
    build_index()
    return {"message": "Data indexed successfully"}

@app.post("/chat")
def chat(request: ChatRequest):
    response =  ask(request.question, session_id=request.session_id)
    return {"answer": response["answer"], "sources": response.get("sources", [])[:2]}