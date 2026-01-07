# backend/vector_store.py

"""
MongoDB Atlas Vector Store

Why MongoDB?
- Stores text, embeddings, and metadata together
- Supports native vector search using cosine similarity
- Free tier is sufficient for prototype-scale RAG systems
"""

from typing import List, Dict
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_collection():
    """
    Create and return the MongoDB collection.
    Connection is created lazily to avoid import-time failures.
    """
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI is not set in environment variables")

    client = MongoClient(mongodb_uri)
    db = client["document_qa"]
    return db["chunks"]


def insert_chunks(chunks_with_embeddings: List[Dict]):
    """
    Insert chunk documents into MongoDB.

    Each document should contain:
    - text
    - embedding (vector)
    - filename
    - page_number
    """
    if not chunks_with_embeddings:
        return

    collection = get_collection()
    collection.insert_many(chunks_with_embeddings)


def clear_collection():
    """
    Remove all documents from the collection.
    Used to reset the knowledge base.
    """
    collection = get_collection()
    collection.delete_many({})


def get_stats() -> Dict:
    """
    Return basic statistics about stored data.
    """
    collection = get_collection()
    total_chunks = collection.count_documents({})
    return {"total_chunks": total_chunks}
