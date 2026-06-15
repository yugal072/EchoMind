Week 1: Core Stabilization (Target: 18–20 June)

Day 1–2: Create rag/index.py + ingest.py (as above)          
                        v'
# Day 3: Clean up technical debt
Fix package structure (__init__.py files)
Remove sys.path hacks
Clean HTML from emails (use BeautifulSoup or html2text)

# Day 4–5: Build minimal FastAPI backend
main.py with two endpoints:
POST /ingest → trigger pipeline
POST /chat → use rag/index.py + Groq LLM


## Day 6–7: Add simple Gradio or Streamlit chat UI (fastest feedback)

Week 1 Success Criteria: You can run the app locally, ingest new data, and chat with it via browser (not just CLI).

# Week 2: Evaluation + Usability (Target: 25 June)

Add basic Evaluation Harness (10–15 test questions)
Add chat history / session memory
Improve metadata filtering (date, source type, sender)
Polish README + add screenshots + demo video

# Also take a look at the evals such as - context retrieval, token management and threshold management

# Days 1–4 (Finish Phase 1b)

Error handling + input validation
Email HTML cleaning
Async ingestion + status endpoint
Pin requirements.txt
Full end-to-end manual testing (ingest 5+ items → multi-turn chat)

# Days 5–10 (Start Phase 2)

Basic Evaluation Harness (10–15 questions + RAGAS/DeepEval)
Metadata filtering (date, source, sender)
Fix in-memory session store (add simple persistence or Redis)
Improve README + add demo screenshots/video





