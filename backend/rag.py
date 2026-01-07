# backend/rag.py

"""
RAG (Retrieval-Augmented Generation)

- Embeds text using Google Gemini
- Retrieves relevant chunks from MongoDB Atlas Vector Search
- Generates grounded answers with citations
"""

from typing import List, Dict
import os
from dotenv import load_dotenv
import google.generativeai as genai

from vector_store import get_collection

# Load environment variables
load_dotenv(override=True)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Models
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "models/gemini-flash-latest"


def embed_text(text: str) -> List[float]:
    """Convert text into an embedding vector using Gemini."""
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return response["embedding"]


def retrieve_chunks(query_embedding: List[float], top_k: int = 8) -> List[Dict]:
    """Retrieve top-k relevant chunks from MongoDB using vector search."""
    collection = get_collection()

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": top_k
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "filename": 1,
                "page_number": 1
            }
        }
    ])

    return list(results)


def generate_answer(question: str, chunks: List[Dict]) -> str:
    """Generate an answer strictly from retrieved context."""
    if not chunks:
        return "I couldn't find this information in the uploaded document."

    context = "\n\n".join(
        f"[Source: {c['filename']}, Page {c['page_number']}]\n{c['text']}"
        for c in chunks
    )

    prompt = f"""You are a helpful assistant that answers questions based on provided document context.

RULES:
1. Answer using ONLY the information in the context below
2. If the question asks about multiple topics, synthesize information from different parts of the context
3. Always include citations in your answer using the format: [Source: filename, Page X]
4. If the information is NOT in the context, respond with: "I couldn't find this information in the uploaded document."
5. Do not use external knowledge

Context:
{context}

Question: {question}

Answer:"""

    model = genai.GenerativeModel(GENERATION_MODEL)
    response = model.generate_content(prompt)

    return response.text.strip()


def ask_question(question: str, top_k: int = 8) -> Dict:
    """
    Full RAG pipeline:
    Embed -> Retrieve -> Generate -> Cite 
    """
    query_embedding = embed_text(question)
    chunks = retrieve_chunks(query_embedding, top_k)
    answer = generate_answer(question, chunks)

    # No citations if answer not found
    if "couldn't find this information" in answer.lower():  #More flexible check
        return {
            "answer": answer,
            "citations": []
        }

    #Proper citation deduplication
    seen = set()
    citations = []

    for c in chunks:
        key = (c["filename"], c["page_number"])
        if key not in seen:
            seen.add(key)
            citations.append({
                "filename": c["filename"],
                "page_number": c["page_number"]
            })

    return {
        "answer": answer,
        "citations": citations
    }

