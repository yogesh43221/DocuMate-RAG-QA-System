# Test Questions & Expected Answers

## Purpose
Test the Document Q&A system with various question types to verify accuracy, grounding, and citation quality based on Test_Doc1.pdf (RAG paper) and Test_Doc2.docx (Hierarchical RL paper).

---

## Test Document 1: RAG Paper (Test_Doc1.pdf)

### 1. What is RAG?
**Question**: "What is RAG?"

**Expected Answer**: 
RAG stands for Retrieval-Augmented Generation. It is a model that combines pre-trained parametric and non-parametric memory for language generation. RAG models use the input sequence to retrieve text documents and use them as additional context when generating the target sequence. The parametric memory is a pre-trained seq2seq model (like BART), and the non-parametric memory is a dense vector index of Wikipedia accessed with a pre-trained neural retriever.

**Citation**: `[Source: Test_Doc1.pdf, Page 1]`

---

### 2. What are the two RAG model variants?
**Question**: "What are the two RAG model variants described in the paper?"

**Expected Answer**:
The paper describes two RAG model variants:
1. **RAG-Sequence**: Uses the same retrieved document to generate the complete sequence
2. **RAG-Token**: Can use different documents to generate different tokens in the sequence

Both models marginalize over retrieved documents to generate outputs.

**Citation**: `[Source: Test_Doc1.pdf, Page 2-3]`

---

### 3. What datasets were used for evaluation?
**Question**: "What datasets were used to evaluate RAG models?"

**Expected Answer**:
RAG models were evaluated on multiple knowledge-intensive tasks including:
- Natural Questions (NQ)
- TriviaQA (TQA)
- WebQuestions (WQ)
- CuratedTrec (CT)
- MS-MARCO for abstractive question answering
- Jeopardy question generation
- FEVER for fact verification

**Citation**: `[Source: Test_Doc1.pdf, Page 4-5]`

---

### 4. What is the retriever component?
**Question**: "What retriever is used in RAG models?"

**Expected Answer**:
RAG uses DPR (Dense Passage Retrieval) as the retriever component. DPR follows a bi-encoder architecture where the retrieval probability p(z|x) is based on BERT encoders. It uses a pre-trained bi-encoder from DPR to initialize the retriever and builds a single MIPS index for Wikipedia using FAISS with Hierarchical Navigable Small World approximation.

**Citation**: `[Source: Test_Doc1.pdf, Page 2-3]`

---

### 5. What generator is used?
**Question**: "What generator model does RAG use?"

**Expected Answer**:
RAG uses BART-large as the generator component, which is a pre-trained seq2seq transformer with 400M parameters. BART was pre-trained using a denoising objective and has obtained state-of-the-art results on a diverse set of generation tasks.

**Citation**: `[Source: Test_Doc1.pdf, Page 3]`

---

### 6. How many documents are retrieved?
**Question**: "How many documents does RAG retrieve during training and testing?"

**Expected Answer**:
During training, RAG retrieves the top K=5 or K=10 documents. For testing, different numbers are used depending on the task: 15 retrieved documents for RAG-Token models on Open-domain QA, and 50 retrieved documents for RAG-Sequence models.

**Citation**: `[Source: Test_Doc1.pdf, Page 3-4]`

---

### 7. RAG performance on Natural Questions
**Question**: "What accuracy did RAG achieve on Natural Questions?"

**Expected Answer**:
RAG-Sequence achieved 44.5% Exact Match score on Natural Questions test set, and RAG-Token achieved 44.1%. This outperformed previous state-of-the-art models including REALM (40.4%) and DPR (41.5%).

**Citation**: `[Source: Test_Doc1.pdf, Page 5-6]`

---

### 8. Negative Test - Out of Scope
**Question**: "What programming language was used to implement RAG?"

**Expected Answer**:
"I couldn't find this information in the uploaded document."

**Citation**: None (out of scope)

---

## Test Document 2: Hierarchical RL Paper (Test_Doc2.docx)

### 9. What is the main contribution of this paper?
**Question**: "What is the main contribution of the hierarchical reinforcement learning paper?"

**Expected Answer**:
The main contribution is using natural language as a way to parameterize the subgoal space in hierarchical reinforcement learning. The paper presents a novel approach where they use data from humans solving tasks to softly supervise the goal space for long-range tasks in a 3D embodied environment. They use unconstrained natural language to represent sub-goals, which is easy to generate from naive human participants and flexible enough to represent a vast range of sub-goals.

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 10. What are the two agent components?
**Question**: "What are the two components of the hierarchical agent?"

**Expected Answer**:
The hierarchical agent has two components:
1. **Low-level (LL) agent**: Produces motor commands for the agent and follows relatively simple language commands
2. **High-level (HL) agent**: Provides subgoals for the agent in the form of language commands

Both use the same architecture. The HL agent issues language commands to the LL agent, which acts as sub-goals in the hierarchical setup.

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 11. What environment was used?
**Question**: "What environment was used for the experiments?"

**Expected Answer**:
The experiments used a 3-D embodied environment in Unity. The tasks are similar to those described in DMLab, where the goal is to find and consume an apple. To acquire the goal apple, the agent must unlock a gate by placing a color-matched key object on a corresponding sensor. The tasks were classified into two Easy and two Hard tasks.

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 12. What losses are used to train the high-level agent?
**Question**: "What losses are used to train the high-level agent?"

**Expected Answer**:
The high-level agent is trained with two losses:
1. **Supervised training loss (BC loss)**: Behavioral cloning loss to match the language commands in the data produced by the 'Setter'
2. **Reinforcement learning loss (RL loss)**: Uses V-trace to optimize language commands for goal-directed behavior based on environment rewards

The total loss combines both: L_HL = w_BC * L_HL_BC + w_RL * L_HL_RL

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 13. How does hierarchical agent compare to flat agent?
**Question**: "How does the hierarchical agent perform compared to the flat agent?"

**Expected Answer**:
The hierarchical agent significantly outperforms the flat agent. The flat agent can pick up on simpler tasks but not on harder tasks, while the hierarchical agent can learn both. The hierarchical agent also learns the easy tasks faster. The flat agent directly produces actions without a hierarchy, while the hierarchical agent produces language instructions every 8 timesteps.

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 14. Are both BC and RL losses necessary?
**Question**: "Are both BC and RL losses necessary for the hierarchical agent?"

**Expected Answer**:
Yes, both losses are necessary. When trained with only BC or only RL loss, the agent cannot learn any of the tasks. The agent trained with both losses learns quickly. The best performance comes from placing comparable weight on both losses. Significantly overweighting one or the other loss leads to poorer performance.

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 15. What is the data collection method?
**Question**: "How was data collected for training the agents?"

**Expected Answer**:
Data was collected using two players: a 'Setter' and a 'Solver'. For the given tasks, a single controllable avatar is controlled by the 'Solver'. The 'Setter' instructs the 'Solver' via a chat interface on how to solve the task. The 'Setter' can observe the 'Solver' but cannot interact with the environment directly. This approach is similar to Abramson et al. [2020].

**Citation**: `[Source: Test_Doc2.docx, Page 1]`

---

### 16. Negative Test - Out of Scope
**Question**: "What is the weather like in the Unity environment?"

**Expected Answer**:
"I couldn't find this information in the uploaded document."

**Citation**: None (out of scope)

---

### 17. Multi-document question
**Question**: "Do both papers use pre-trained models?"

**Expected Answer**:
Yes, both papers use pre-trained models. The RAG paper uses pre-trained BART-large as the generator and pre-trained DPR as the retriever. The hierarchical RL paper pre-trains the low-level agent to follow language commands by imitating expert humans on a large range of language conditional tasks.

**Citation**: `[Source: Test_Doc1.pdf, Page 3]` and `[Source: Test_Doc2.docx, Page 1]`

---

## Quick Reference Summary

### Test_Doc1.pdf (RAG Paper) - Key Facts:
- RAG = Retrieval-Augmented Generation
- Two variants: RAG-Sequence and RAG-Token
- Uses BART-large (400M params) as generator
- Uses DPR as retriever with Wikipedia index
- Retrieves top-5 or top-10 documents during training
- Achieves 44.5% EM on Natural Questions
- Evaluated on NQ, TriviaQA, WebQuestions, CuratedTrec, MS-MARCO, Jeopardy, FEVER

### Test_Doc2.docx (Hierarchical RL Paper) - Key Facts:
- Uses natural language for subgoal parameterization
- Two agents: Low-level (motor commands) and High-level (language subgoals)
- Environment: 3D Unity environment with key-gate-apple tasks
- Training: BC loss + RL loss (both necessary)
- Data collection: 'Setter' (instructor) + 'Solver' (executor)
- Hierarchical agent outperforms flat agent
- Hard tasks require more diverse instructions than easy tasks

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