# frontend/app.py

import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Document Q&A Assistant", layout="wide")

st.title("📝 Document Q&A Assistant")
st.write("Upload a document (PDF, DOCX, TXT, Markdown) and ask questions based on its content.")

# Sidebar
st.sidebar.header("📤 Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload a document", 
    type=["pdf", "docx", "txt", "md", "markdown"]
)

# Upload logic
if uploaded_file is not None:
    with st.spinner("Uploading and indexing document..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)

    if response.status_code == 200:
        result = response.json()
        st.sidebar.success("✅ Indexed successfully!")
        st.sidebar.info(f"📊 {result['chunks_created']} chunks created")
    else:
        st.sidebar.error(response.json().get("detail", "Upload failed"))

st.sidebar.divider()

# Show current knowledge base status
try:
    status_response = requests.get(f"{BACKEND_URL}/status")
    if status_response.status_code == 200:
        status_data = status_response.json()
        if status_data["total_chunks"] > 0:
            st.sidebar.markdown("### 📚 Knowledge Base")
            st.sidebar.metric("Documents", status_data["total_documents"])
            st.sidebar.metric("Total Chunks", status_data["total_chunks"])
            
            # Show list of uploaded documents
            if "documents" in status_data and status_data["documents"]:
                st.sidebar.markdown("**Uploaded Documents:**")
                for doc in status_data["documents"]:
                    st.sidebar.text(f"• {doc}")
        else:
            st.sidebar.info("📭 No documents indexed")
except:
    pass

st.sidebar.divider()

if st.sidebar.button("Reset Knowledge Base"):
    res = requests.delete(f"{BACKEND_URL}/reset")
    if res.status_code == 200:
        st.sidebar.success("Knowledge base reset successfully")
        st.rerun()
    else:
        st.sidebar.error("Failed to reset knowledge base")

# Chat section
st.header("💬 Ask a Question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if uploaded_file is None and not st.session_state.chat_history:
    st.info("👈 Upload a document from the sidebar to get started.")

# Clear input box if clear was clicked
default_question = "" if st.session_state.clear_input else None
question = st.text_input("Enter your question", value=default_question, key="question_input")

# Reset clear flag after rendering
if st.session_state.clear_input:
    st.session_state.clear_input = False

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {"question": question, "top_k": 5}
        response = requests.post(f"{BACKEND_URL}/ask", json=payload)

        if response.status_code == 200:
            result = response.json()
            # Clear previous history and show only current answer
            st.session_state.chat_history = [result]
        else:
            st.error(response.json().get("detail", "Error answering question"))

# Display chat history
for item in st.session_state.chat_history:
    st.markdown("### ✅ Answer")
    st.write(item["answer"])

    if item["sources"]:
        st.markdown("**Sources:**")
        for src in item["sources"]:
            st.write(f"- {src['filename']} (Page {src['page_number']})")

st.divider()

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.clear_input = True
    st.rerun()
