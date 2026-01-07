# Architecture Diagram Instructions

Create a visual diagram showing the RAG system flow. Use tools like:
- [Excalidraw](https://excalidraw.com) (recommended - simple, fast)
- [Draw.io](https://draw.io)
- [Lucidchart](https://lucidchart.com)

## Diagram Content

### Two Main Flows

#### Flow 1: Document Indexing (Left Side)
```
User (Streamlit UI)
    ↓ [Upload PDF]
FastAPI Backend
    ↓ [Extract]
PDF Text Extraction (PyPDF2)
    ↓ [Chunk]
Text Chunking (750 tokens, 100 overlap)
    ↓ [Embed]
OpenAI API (text-embedding-3-small)
    ↓ [Store]
MongoDB Atlas (Vector Index)
    ↓
"Document Indexed ✓"
```

#### Flow 2: Question Answering (Right Side)
```
User Question (Streamlit UI)
    ↓ [Embed Query]
OpenAI API (text-embedding-3-small)
    ↓ [Vector Search]
MongoDB Atlas (Cosine Similarity)
    ↓ [Top-5 Chunks]
Retrieved Context
    ↓ [Generate]
OpenAI API (GPT-4o-mini)
    ↓ [Format]
Answer + Citations
    ↓
Display to User
```

## Visual Style

**Colors** (use these for clarity):
- **Blue**: User interactions (Streamlit)
- **Green**: OpenAI API calls
- **Orange**: MongoDB operations
- **Gray**: Processing steps (chunking, extraction)

**Boxes**:
- Rectangle: Processing steps
- Rounded rectangle: Services (APIs, databases)
- Diamond: Decision points (if any)

**Arrows**:
- Solid arrows with labels showing data flow
- Label each arrow with what's being passed

## Key Components to Highlight

### 1. Technology Stack (top of diagram)
```
Frontend: Streamlit
Backend: FastAPI
LLM: OpenAI GPT-4o-mini
Embeddings: text-embedding-3-small (1536D)
Vector DB: MongoDB Atlas
```

### 2. Data Flow Labels
- "PDF bytes" → Extract
- "Raw text + page numbers" → Chunk
- "Text chunks (750 tokens)" → Embed
- "Embeddings (1536D vectors)" → Store
- "Query text" → Embed
- "Query vector" → Search
- "Top-5 chunks + metadata" → Generate
- "Answer + [Source: file, Page X]" → Display

### 3. Key Annotations
Add text boxes with:
- "Chunk size: 750 tokens, 100 overlap"
- "Top-K: 5 chunks retrieved"
- "Cosine similarity for vector search"
- "Citations: [Source: filename, Page X]"

## Export

- Export as PNG (1920x1080 or higher)
- Name it `architecture.png`
- Place in project root directory

## Interview Explanation (Practice This)

> "The system has two main flows. First, document indexing: when a user uploads a PDF, we extract text with page tracking, chunk it into 750-token pieces with 100-token overlap, generate embeddings using OpenAI's text-embedding-3-small model, and store them in MongoDB Atlas with a vector index.
>
> Second, question answering: when the user asks a question, we embed it using the same model, perform a vector search in MongoDB using cosine similarity to find the top 5 most relevant chunks, pass those chunks to GPT-4o-mini with a strict prompt to answer only from the context, and return the answer with citations showing the source file and page number.
>
> The key insight is that we're not training a model—we're retrieving relevant information and letting the LLM synthesize it with proper grounding."

## Quick Excalidraw Steps

1. Go to excalidraw.com
2. Create two columns (left = indexing, right = querying)
3. Add rectangles for each step
4. Connect with arrows
5. Add labels on arrows
6. Use colors: blue (UI), green (OpenAI), orange (MongoDB)
7. Add title at top: "Document Q&A RAG System Architecture"
8. Export as PNG

**Time estimate**: 15-20 minutes for a clean diagram