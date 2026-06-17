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
- The meatadata filtering is not supporting the sender and subject sections due to limitation of ChromaDB
Fix in-memory session store (add simple persistence or Redis)  
Improve README + add demo screenshots/video



# ================================================================================================================================================
# ================================================================================================================================================


# Phase 1: Core Stability & Usable MVP (Current Phase – Target: 7–10 days)
Goal: Make the current system reliable, deduplicated, persistent, and user-friendly.
Step-by-Step Tasks:

1. Deduplication & Ingestion Robustness (2–3 days)
Fix ID generation for chunks (PDFs, emails, files)
Add proper check so it doesn’t re-process unchanged data
Add logging: “Added X new chunks, skipped Y duplicates”

2. Metadata Enrichment (1–2 days)
Attach rich metadata (source, date, sender, subject, filename, ingested_at)
Improve metadata during parsing

3. Metadata Filtering in Retriever (2 days)
Implement build_metadata_filter() properly
Support date range, source, sender filtering
Integrate into the RAG chain

4. Session Persistence (2 days)
Replace in-memory store with JSON file or SQLite persistence
History survives server restart

5. File Upload from Streamlit UI (2 days)
Allow users to upload PDFs, text files, audio from the UI
Trigger ingestion automatically


# Phase 1 Success Criteria:

No duplicate chunks on re-ingestion
Metadata filtering works (e.g., “show emails from last week”)
Chat history persists after restart
Users can upload files from UI


# Phase 2: Quality & Evaluation (Next 7–10 days)
Goal: Make the RAG actually good and measurable.
Key Tasks:

Build a simple custom evaluator (Faithfulness + Answer Relevancy)
Create generate_test_results.py script
Improve system prompt significantly based on evaluation
Add Hybrid Search (after moving to Qdrant)
Run evaluation after every major change and track scores

Success Criteria:

Faithfulness ≥ 0.85
Answer Relevancy ≥ 0.75
You have a repeatable evaluation process


# Phase 3: More Data Sources & Near Real-time (2–3 weeks)
Goal: Expand ingestion capabilities.
Tasks:

WhatsApp chat export ingestion (manual upload first)
Audio transcription + ingestion (Whisper)
SMS export support
Calendar integration (Google Calendar)
Notes / Obsidian / other file types

Success Criteria:

User can upload WhatsApp exports and audio files from UI
All sources feed into the same unified knowledge base


# Phase 4: Agentic Capabilities (2–3 weeks)
Goal: Turn EchoMind from a search tool into a true assistant.
Tasks:

Implement LangGraph agent with tools
Tools: web search, draft email, create calendar event, summarize week, find deadlines, etc.
Add reflection/critic loop for better quality
Long-term memory (user profile, preferences)

Success Criteria:

User can say: “Summarize my important emails this week”, “Draft reply to last email from boss”, “What are my deadlines in next 7 days?”


# Phase 5: Production & Advanced Features (3–4 weeks)
Tasks:

Move to Qdrant (better filtering + hybrid search)
Add GraphDB (Neo4j or simple graph layer) for relationships
Docker + Docker Compose
Better UI (optional React)
Proactive notifications (deadlines, follow-ups)
Privacy controls (delete cache, selective memory)
Deployment (Railway / AWS / Vercel)

