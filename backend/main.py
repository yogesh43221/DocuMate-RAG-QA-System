# backend/main.py

"""
FastAPI Backend for Document Q&A (RAG) System

Endpoints:
- POST /upload : Upload and index PDF
- POST /ask    : Ask questions
- DELETE /reset: Clear knowledge base
- GET /status  : System status
"""

import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from ingestion import extract_document, chunk_text
from rag import embed_text, ask_question
from vector_store import insert_chunks, clear_collection, get_stats, get_collection

# Load environment variables from .env or Streamlit secrets
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Running on Streamlit Cloud
        os.environ['GEMINI_API_KEY'] = st.secrets.get('GEMINI_API_KEY', '')
        os.environ['MONGODB_URI'] = st.secrets.get('MONGODB_URI', '')
except:
    pass

# Fallback to .env file
if not os.getenv('GEMINI_API_KEY'):
    load_dotenv()

app = FastAPI(title="Document Q&A API")

# Allow frontend (Streamlit) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for prototype
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.get("/status")
def status():
    stats = get_stats()
    collection = get_collection()
    unique_docs = collection.distinct("filename")

    return {
        "total_chunks": stats["total_chunks"],
        "total_documents": len(unique_docs),
        "documents": unique_docs,  # Add list of document names
        "status": "active" if stats["total_chunks"] > 0 else "empty"
    }


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document.
    Supports: PDF, DOCX, TXT, Markdown
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt', '.md', '.markdown']
    file_ext = '.' + file.filename.lower().split('.')[-1]
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Supported formats: PDF, DOCX, TXT, Markdown"
        )
    
    # Absolute upload path (safe)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir = os.path.join(base_dir, "data", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    try:
        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract + chunk (works for all formats)
        pages = extract_document(file_path)
        chunks = chunk_text(pages)

        # Generate embeddings & store
        documents = []
        for chunk in chunks:
            embedding = embed_text(chunk["text"])
            documents.append({
                "text": chunk["text"],
                "embedding": embedding,
                "filename": chunk["filename"],
                "page_number": chunk["page_number"]
            })

        insert_chunks(documents)

        return {
            "message": "Document indexed successfully",
            "filename": file.filename,
            "chunks_created": len(documents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def ask(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = ask_question(request.question, request.top_k)

        return {
            "answer": result["answer"],
            "sources": result["citations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/reset")
def reset():
    clear_collection()
    return {"message": "Knowledge base reset successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
