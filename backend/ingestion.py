# backend/ingestion.py

from typing import List, Dict
import os
from PyPDF2 import PdfReader
from docx import Document

def extract_pdf_with_pages(pdf_path: str) -> List[Dict]:
    """
    Extract text from a PDF file page by page.
    Each page keeps its page number for citations.
    """
    reader = PdfReader(pdf_path)
    filename = os.path.basename(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "text": text,
                "page_number": page_number,
                "filename": filename
            })
    return pages


def extract_docx(docx_path: str) -> List[Dict]:
    """
    Extract text from a DOCX file.
    Treats entire document as page 1.
    """
    doc = Document(docx_path)
    filename = os.path.basename(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    
    if text.strip():
        return [{"text": text, "page_number": 1, "filename": filename}]
    return []


def extract_txt(txt_path: str) -> List[Dict]:
    """
    Extract text from a TXT file.
    Treats entire file as page 1.
    """
    filename = os.path.basename(txt_path)
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    if text.strip():
        return [{"text": text, "page_number": 1, "filename": filename}]
    return []


def extract_markdown(md_path: str) -> List[Dict]:
    """
    Extract text from a Markdown file.
    Treats entire file as page 1.
    """
    filename = os.path.basename(md_path)
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    if text.strip():
        return [{"text": text, "page_number": 1, "filename": filename}]
    return []


def extract_document(file_path: str) -> List[Dict]:
    """
    Route to appropriate extractor based on file extension.
    Supports: PDF, DOCX, TXT, Markdown
    """
    ext = file_path.lower().split('.')[-1]
    
    if ext == 'pdf':
        return extract_pdf_with_pages(file_path)
    elif ext == 'docx':
        return extract_docx(file_path)
    elif ext == 'txt':
        return extract_txt(file_path)
    elif ext in ['md', 'markdown']:
        return extract_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")


def chunk_text(
    pages: List[Dict],
    chunk_size: int = 750,
    overlap: int = 100
) -> List[Dict]:
    """
    Split text into overlapping chunks.
    Chunking helps retrieval accuracy and keeps context manageable.
    """
    chunks = []

    for page in pages:
        words = page["text"].split()
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunks.append({
                "text": " ".join(chunk_words),
                "page_number": page["page_number"],
                "filename": page["filename"]
            })

            #start = end - overlap
            start = max(end - overlap, start + 1)   #To avoid infine loop when overlap >= chunk_size

    return chunks










# """
# Document ingestion pipeline: Extract -> Chunk -> Embed -> Store
# """
# import PyPDF2
# from typing import List, Dict
# import openai
# import os
# from datetime import datetime

# # Initialize OpenAI client
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def extract_pdf_with_pages(filepath: str) -> List[Dict]:
#     """
#     Extract text from PDF with page tracking.
    
#     Args:
#         filepath: Path to PDF file
        
#     Returns:
#         List of dicts with 'text' and 'page_number'
#     """
#     chunks = []
#     try:
#         with open(filepath, 'rb') as f:
#             reader = PyPDF2.PdfReader(f)
#             for page_num, page in enumerate(reader.pages, start=1):
#                 text = page.extract_text()
#                 if text.strip():  # Only add non-empty pages
#                     chunks.append({
#                         "text": text,
#                         "page_number": page_num
#                     })
#         return chunks
#     except Exception as e:
#         raise Exception(f"PDF extraction failed: {str(e)}")


# def chunk_text(page_data: List[Dict], chunk_size: int = 750, overlap: int = 100) -> List[Dict]:
#     """
#     Split text into overlapping chunks while preserving page numbers.
    
#     Args:
#         page_data: List of dicts with 'text' and 'page_number'
#         chunk_size: Target tokens per chunk (default: 750)
#         overlap: Overlap tokens between chunks (default: 100)
        
#     Returns:
#         List of dicts with 'text', 'page_number', 'chunk_index'
#     """
#     chunks = []
#     chunk_index = 0
    
#     for page in page_data:
#         text = page["text"]
#         page_num = page["page_number"]
        
#         # Simple token approximation: 1 token ≈ 4 characters
#         words = text.split()
#         chars_per_chunk = chunk_size * 4
#         chars_overlap = overlap * 4
        
#         start = 0
#         while start < len(text):
#             end = start + chars_per_chunk
#             chunk_text = text[start:end]
            
#             if chunk_text.strip():
#                 chunks.append({
#                     "text": chunk_text,
#                     "page_number": page_num,
#                     "chunk_index": chunk_index
#                 })
#                 chunk_index += 1
            
#             # Move start forward with overlap
#             start = end - chars_overlap
#             if start >= len(text):
#                 break
    
#     return chunks


# def generate_embeddings(text: str) -> List[float]:
#     """
#     Generate embeddings using OpenAI.
    
#     Args:
#         text: Text to embed
        
#     Returns:
#         Embedding vector (1536 dimensions)
#     """
#     try:
#         response = client.embeddings.create(
#             input=text,
#             model="text-embedding-3-small"
#         )
#         return response.data[0].embedding
#     except Exception as e:
#         raise Exception(f"Embedding generation failed: {str(e)}")


# def process_document(filepath: str, filename: str) -> List[Dict]:
#     """
#     Complete ingestion pipeline for a document.
    
#     Args:
#         filepath: Path to document file
#         filename: Original filename
        
#     Returns:
#         List of processed chunks ready for MongoDB insertion
#     """
#     # Step 1: Extract text with page numbers
#     page_data = extract_pdf_with_pages(filepath)
    
#     # Step 2: Chunk the text
#     chunks = chunk_text(page_data)
    
#     # Step 3: Generate embeddings and prepare for storage
#     processed_chunks = []
#     for chunk in chunks:
#         embedding = generate_embeddings(chunk["text"])
        
#         processed_chunks.append({
#             "text": chunk["text"],
#             "embedding": embedding,
#             "metadata": {
#                 "filename": filename,
#                 "page_number": chunk["page_number"],
#                 "chunk_index": chunk["chunk_index"],
#                 "uploaded_at": datetime.utcnow().isoformat()
#             }
#         })
    
#     return processed_chunks