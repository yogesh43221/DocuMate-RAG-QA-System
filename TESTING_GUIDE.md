# Testing Guide - Multi-Format Support

## Installation

Before testing, install the new dependency:

```bash
cd backend
pip install python-docx==1.1.0
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

## Test Files Provided

The `data/uploads/` folder contains test files:
- `rag_test_document.pdf` - PDF format
- `test_document.txt` - TXT format
- `test_document.md` - Markdown format

## Testing Steps

### 1. Start Backend
```bash
cd backend
python main.py
```

### 2. Start Frontend (new terminal)
```bash
cd frontend
streamlit run app.py
```

### 3. Test Each Format

#### Test PDF Upload
1. Upload `rag_test_document.pdf`
2. Ask: "What is a smart city?"
3. Expected: Answer with citation `[Source: rag_test_document.pdf, Page 1]`

#### Test TXT Upload
1. Click "Reset Knowledge Base"
2. Upload `test_document.txt`
3. Ask: "What technologies are used in smart cities?"
4. Expected: Answer with citation `[Source: test_document.txt, Page 1]`

#### Test Markdown Upload
1. Click "Reset Knowledge Base"
2. Upload `test_document.md`
3. Ask: "What challenges do smart cities face?"
4. Expected: Answer with citation `[Source: test_document.md, Page 1]`

#### Test DOCX Upload (if you have a DOCX file)
1. Create a simple DOCX file with some text
2. Upload it
3. Ask questions about the content
4. Expected: Answer with citation `[Source: yourfile.docx, Page 1]`

### 4. Test "Not Found" Scenario
With any document uploaded, ask:
- "What is the weather today?"
- Expected: "I couldn't find this information in the uploaded document."
- Expected: No sources displayed

## Verification Checklist

- [ ] PDF files upload successfully
- [ ] DOCX files upload successfully
- [ ] TXT files upload successfully
- [ ] Markdown files upload successfully
- [ ] Questions are answered with citations
- [ ] Citations show correct filename
- [ ] "Not found" message works
- [ ] Clear Chat works
- [ ] Reset KB works

## Common Issues

### "ModuleNotFoundError: No module named 'docx'"
**Fix:** Run `pip install python-docx==1.1.0`

### "Unsupported file type"
**Fix:** Ensure file extension is .pdf, .docx, .txt, .md, or .markdown

### DOCX extraction returns empty
**Fix:** Ensure DOCX file has actual text content (not just images)

## Success Criteria

✅ All 4 file formats upload and index successfully
✅ Questions answered with proper citations
✅ Filename shown correctly in citations
✅ "Not found" message for out-of-scope questions
✅ No errors in backend logs
