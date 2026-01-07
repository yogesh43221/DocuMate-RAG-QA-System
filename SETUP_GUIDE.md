# Complete Setup Guide

## Prerequisites Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Internet connection
- [ ] Text editor (VS Code recommended)

---

## Step 1: Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Name it "Document-QA-RAG"
6. Copy the key (starts with `sk-`)
7. **Save it securely** - you can't see it again!

**Cost estimate**: ~$0.10 for testing with a few documents

---

## Step 2: Setup MongoDB Atlas

### 2.1 Create Account
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Try Free"
3. Sign up with email or Google
4. Choose the **FREE tier** (M0)

### 2.2 Create Cluster
1. Choose cloud provider: **AWS** (recommended)
2. Choose region: **Closest to you**
3. Cluster name: `DocumentQA` (or keep default)
4. Click "Create"
5. Wait 3-5 minutes for cluster to deploy

### 2.3 Setup Database Access
1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Username: `rag_user`
4. Password: Click "Autogenerate Secure Password"
5. **Copy and save the password**
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

### 2.4 Setup Network Access
1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Or add your current IP
5. Click "Confirm"

### 2.5 Create Database and Collection
1. Go to "Database" in left sidebar
2. Click "Browse Collections"
3. Click "Add My Own Data"
4. Database name: `document_qa`
5. Collection name: `chunks`
6. Click "Create"

### 2.6 Create Vector Search Index
1. In the `chunks` collection, click "Search Indexes" tab
2. Click "Create Search Index"
3. Choose "JSON Editor"
4. Index name: `vector_index`
5. Paste this configuration:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

6. Click "Next"
7. Click "Create Search Index"
8. Wait for status to become "Active" (~2 minutes)

### 2.7 Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Driver: **Python**, Version: **3.12 or later**
4. Copy the connection string
5. It looks like: `mongodb+srv://rag_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`
6. **Replace `<password>` with your actual password** from step 2.3

---

## Step 3: Setup Project

### 3.1 Create Project Structure
```bash
mkdir document-qa-rag
cd document-qa-rag

mkdir backend frontend data data/uploads
```

### 3.2 Create Files
Copy the code provided into these files:
- `backend/main.py`
- `backend/ingestion.py`
- `backend/rag.py`
- `backend/requirements.txt`
- `frontend/app.py`
- `frontend/requirements.txt`
- `README.md`
- `test_questions.md`

### 3.3 Create .env File
```bash
# In project root
touch .env
```

Edit `.env` with your keys:
```
OPENAI_API_KEY=sk-your-actual-key-here
MONGODB_URI=mongodb+srv://rag_user:your-password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Important**: Replace `your-actual-key-here` and `your-password` with real values!

---

## Step 4: Install Dependencies

### 4.1 Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**If you get errors**, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.2 Frontend Dependencies
```bash
cd ../frontend
pip install -r requirements.txt
```

---

## Step 5: Test Backend

### 5.1 Start Backend
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5.2 Test Health Check
Open browser to: http://localhost:8000

You should see:
```json
{"status": "Document Q&A API is running"}
```

### 5.3 Test Status Endpoint
Open browser to: http://localhost:8000/status

You should see:
```json
{
  "total_chunks": 0,
  "total_documents": 0,
  "status": "empty"
}
```

**If this works, your backend is ready!** ✅

---

## Step 6: Test Frontend

### 6.1 Start Frontend (New Terminal)
```bash
cd frontend
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Browser should auto-open. If not, go to: http://localhost:8501

### 6.2 Verify UI
You should see:
- Title: "Document Q&A Assistant"
- Sidebar with upload section
- Empty chat interface
- Status: "Knowledge base is empty"

**If this works, your frontend is ready!** ✅

---

## Step 7: First Test Run

### 7.1 Prepare Test Document
Find or create a simple PDF (e.g., a company policy, resume, or article)

### 7.2 Upload Document
1. Click "Choose a PDF file" in sidebar
2. Select your PDF
3. Click "Index Document"
4. Wait for "Document indexed successfully" message
5. Check status - should show document and chunk count

### 7.3 Ask First Question
Type a simple question based on your document:
- "What is this document about?"
- "Summarize the main points"

Expected: Answer with citation like `[Source: yourfile.pdf, Page 1]`

### 7.4 Test "Not Found"
Ask something NOT in the document:
- "What is the weather today?"

Expected: "I couldn't find this information in the uploaded document."

**If both work, you're done!** 🎉

---

## Common Issues & Fixes

### Issue 1: "Cannot connect to backend"
**Fix**:
1. Make sure backend is running (`python main.py` in backend/)
2. Check if port 8000 is free
3. Try: `lsof -i :8000` and kill any process using it

### Issue 2: "OpenAI API error"
**Fix**:
1. Verify `.env` file is in project root
2. Check API key is correct (no extra spaces)
3. Verify you have credits in OpenAI account
4. Try: `echo $OPENAI_API_KEY` to verify environment variable

### Issue 3: "MongoDB connection error"
**Fix**:
1. Check connection string format
2. Verify password has no special characters (if so, URL-encode them)
3. Confirm IP is whitelisted in Atlas
4. Test connection in MongoDB Compass

### Issue 4: "Vector search failed"
**Fix**:
1. Verify vector index is "Active" in Atlas
2. Check index name is exactly `vector_index`
3. Verify `numDimensions: 1536` in index config
4. Wait 2-3 minutes after index creation

### Issue 5: "Module not found"
**Fix**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue 6: PDF extraction fails
**Fix**:
1. Try a different PDF (some are image-based)
2. Ensure PDF is not password-protected
3. Check file size (<50MB recommended)

---

## Verification Checklist

Before submitting, verify:

- [ ] Backend runs without errors
- [ ] Frontend loads correctly
- [ ] Can upload PDF successfully
- [ ] Document gets indexed (shows chunk count)
- [ ] Can ask questions and get answers with citations
- [ ] "Not found" message works for out-of-scope questions
- [ ] Clear Chat button works
- [ ] Reset KB button works
- [ ] README is complete
- [ ] Test questions documented
- [ ] Architecture diagram created
- [ ] Demo video recorded

---

## Ready for Demo!

Your system is now ready. Practice your 2-minute explanation:

1. **Upload** a document (30 sec)
2. **Ask** 2-3 questions showing citations (1 min)
3. **Explain** architecture briefly (30 sec)

Good luck! 🚀