# Test Questions & Expected Behavior

## Purpose
Test the Document Q&A system with various question types to verify accuracy, grounding, and citation quality.

---

## Test Document: Company Employee Handbook

### 1. Direct Factual Question
**Question**: "What is the vacation policy?"

**Expected Behavior**:
- Extract specific vacation days/hours
- Include citation: `[Source: handbook.pdf, Page X]`
- Should NOT add information not in the document

**Success Criteria**: Answer matches document exactly with correct page reference

---

### 2. Multi-Section Question
**Question**: "What benefits does the company offer?"

**Expected Behavior**:
- May retrieve multiple chunks (health insurance, 401k, etc.)
- Citations from multiple pages if benefits span sections
- Synthesize information coherently

**Success Criteria**: Comprehensive list with multiple citations

---

### 3. Negative Test (Out of Scope)
**Question**: "What is the company's stock price?"

**Expected Behavior**:
- Response: "I couldn't find this information in the uploaded document."
- NO hallucination or external knowledge
- NO citation

**Success Criteria**: Refuses to answer without making up information

---

### 4. Implicit Information
**Question**: "Can I work from home?"

**Expected Behavior**:
- Find "remote work policy" or "work from home" section
- Cite the relevant page
- If policy is unclear, quote exactly what document says

**Success Criteria**: Grounded answer about remote work policy

---

### 5. Numerical Data
**Question**: "How many sick days do employees get per year?"

**Expected Behavior**:
- Extract exact number
- Citation with page number
- No approximation or assumption

**Success Criteria**: Precise number with source

---

### 6. Conditional Information
**Question**: "What happens if I resign without notice?"

**Expected Behavior**:
- Find resignation/termination policy
- Quote consequences or procedures
- Citation with page

**Success Criteria**: Accurate policy details with source

---

### 7. Comparison Question
**Question**: "What's the difference between sick leave and vacation time?"

**Expected Behavior**:
- Retrieve chunks about both policies
- Contrast the two clearly
- Citations for both sections

**Success Criteria**: Clear comparison with dual citations

---

### 8. Ambiguous Question
**Question**: "What about parking?"

**Expected Behavior**:
- Find parking policy/benefits section
- Provide details if available
- If not found: "I couldn't find this information..."

**Success Criteria**: Handles ambiguity appropriately

---

### 9. Long-Form Question
**Question**: "What is the process for requesting time off and how far in advance should I submit the request?"

**Expected Behavior**:
- Retrieve relevant PTO/leave request process
- Multi-part answer addressing both aspects
- Citations for each part

**Success Criteria**: Complete answer with proper structure

---

### 10. Edge Case (Information at Page Boundary)
**Question**: "What is the dress code policy?"

**Expected Behavior**:
- Should work even if policy spans page break
- 100-token overlap should capture complete context
- Citation may reference first page where policy starts

**Success Criteria**: Complete answer without information cutoff

---

## Evaluation Rubric

### Accuracy & Grounding (40%)
- [ ] Answers are factually correct per document
- [ ] No hallucinated information
- [ ] Handles "not found" cases appropriately
- [ ] No external knowledge injected

### Citation Quality (20%)
- [ ] Every answer has citations
- [ ] Citations show filename and page number
- [ ] Citations are accurate (verifiable)
- [ ] Format: `[Source: filename.pdf, Page X]`

### User Experience (20%)
- [ ] Answers are clear and concise
- [ ] Appropriate handling of ambiguous questions
- [ ] Fast response time (<5 seconds)
- [ ] UI is intuitive

### Code Quality (20%)
- [ ] Clean, documented code
- [ ] Proper error handling
- [ ] Modular structure
- [ ] Easy to set up and run

---

## Additional Test Scenarios

### Upload & Indexing
1. Upload valid PDF → Should succeed with chunk count
2. Upload non-PDF → Should reject with clear error
3. Upload corrupted PDF → Should handle gracefully
4. Upload very large PDF (>50 pages) → Should show progress

### Knowledge Base Management
1. Clear Chat → Conversation resets, documents remain
2. Reset KB → All documents deleted, confirmation required
3. Multiple uploads → Should accumulate or replace (verify behavior)

### Edge Cases
1. Empty question → Should prompt for input
2. Question with special characters → Should handle
3. Very long question (>500 words) → Should process or truncate
4. Simultaneous users (if deployed) → Verify isolation

---

## Demo Script (3-5 Minutes)

### Part 1: Upload (30 seconds)
1. Show empty knowledge base status
2. Upload sample PDF
3. Wait for indexing confirmation
4. Show chunk count

### Part 2: Questioning (2 minutes)
1. Ask direct factual question → Show citation
2. Ask out-of-scope question → Show "not found" message
3. Ask complex question → Show multi-source answer
4. Expand sources to show page numbers

### Part 3: Features (1 minute)
1. Demonstrate "Clear Chat" button
2. Demonstrate "Reset KB" button
3. Show Top-K slider (if implemented)

### Part 4: Architecture Explanation (1-2 minutes)
- Show README diagram
- Explain: Index → Retrieve → Generate
- Mention key decisions (750 tokens, Top-5, citations)

---

## Success Metrics

**Minimum to Pass**:
- 8/10 test questions answered correctly with citations
- 0 hallucinations
- "Not found" works for out-of-scope questions
- Clean UI, working upload/reset

**Excellence Indicators**:
- 10/10 questions correct
- Fast response (<3 seconds)
- Clear, professional UI
- Well-documented code
- Thoughtful README