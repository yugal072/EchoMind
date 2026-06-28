# EchoMind RAG System: Metadata Filtering & Qdrant Migration Report

**Date**: June 28, 2026

## 1. Aim and Problem Statement

The goal of this session was to resolve silent failures and limitations in the metadata filtering logic of the EchoMind RAG system. The system ingested documents from multiple sources (Gmail, Calendar, PDFs, Plain text, Obsidian, and Voice Notes). However, during the RAG retrieval phase, metadata filters extracted from natural language queries were not being properly applied. 

**Key Problems:**
1. **Qdrant Embedded Mode Limitations:** The system used local embedded Qdrant (`path="..."`). Local Qdrant lacks support for Payload Indexes, which are required for `$contains` (substring/full-text matching) queries. This caused substring searches on fields like `sender` and `subject` to fail silently.
2. **Inconsistent Metadata:** Different loaders were not attaching unified metadata. The RAG filter generator expected fields like `subject` and `date_ts`, but parsers for Calendar, Obsidian, Audio, and local Files were either using different naming conventions (e.g., `summary`, `note_title`) or were missing timestamps entirely. 
3. **ID Generation Collisions:** The pipeline hash generator for PDFs and Files mistakenly used the literal strings `"pdf"` or `"file"` instead of the actual filename, leading to ID overwrites in the vector store.
4. **LangChain Nested Metadata:** LangChain's Qdrant vector store implementation natively nests document metadata inside a `"metadata"` JSON key inside the Qdrant payload, which broke custom native Qdrant filters that tried to search at the root of the payload.

---

## 2. Solutions and Fixes Implemented

### 2.1 Qdrant Server Migration
- **Solution:** Migrated from embedded Qdrant to a standalone Qdrant Server (`http://localhost:6333`). 
- **Implementation:** Updated `get_vectorstore()` in `app/RAG/index.py` to use `url="http://localhost:6333"` and configured it to create payload indexes for `metadata.source`, `metadata.sender`, and `metadata.subject` unconditionally when creating the vector store collection.

### 2.2 Standardizing Metadata
Modified all parsers inside `app/ingestion/` to provide consistent aliases so the RAG pipeline could seamlessly filter any document type:
- **`pipeline.py` (PDF & Text):** Added `subject` (aliased to filename) and `date_ts` (using OS file modification time or ingestion time). Fixed the ID collision bug by ensuring `filename` is hashed instead of the literal `source` string.
- **`calender_parser.py`:** Added `subject` (aliased to the event `summary`) and parsed the Google Calendar ISO string to an Epoch `date_ts` float.
- **`obsidian_parser.py`:** Added `subject` (aliased to `note_title`) and captured the OS `st_mtime` for the `date_ts` float.
- **`audio.py`:** Added `subject` (aliased to the audio filename) and used ingestion time as `date_ts`.

### 2.3 Fixing LangChain Metadata Nesting Queries
- **Solution:** Modified `app/RAG/metadatas/qdrant_translator.py`.
- **Implementation:** Updated `to_qdrant_filter()` to automatically prepend `metadata.` to all filter condition keys (e.g., `metadata.subject`). This correctly routes native Qdrant filter parameters into LangChain's nested metadata dictionary.

### 2.4 API Schema Expansion
- **Solution:** Extended the `ChatRequest` schema in `app/main.py` so that users or front-end clients can manually override extended filters (`tags`, `folder`, `language`, `location`) alongside traditional filters. 

---

## 3. Execution Process

To run the full stack and populate the system properly, follow these steps:

### Step 1: Start the Qdrant Server
Qdrant must be running in standalone server mode before the backend or ingestion scripts can be used.
1. Open a terminal.
2. Navigate to your Qdrant tool directory: `cd D:\tools\qdrant`
3. Execute the server binary:
   ```powershell
   # Windows PowerShell
   .\qdrant.exe
   ```
   *The server will start and listen on port `6333`.*

### Step 2: Run the Ingestion Pipeline
To backfill documents into the Qdrant server, execute the ingestion script. Because Windows CMD / PowerShell can crash when trying to print Unicode emoji characters using the default `cp1252` encoding, you must force UTF-8.
1. Open a new terminal.
2. Navigate to your backend directory: `cd D:\PROJECTS\GenAI\EchoMind\backend`
3. Force UTF-8 and run ingestion:
   ```powershell
   # Windows PowerShell
   $env:PYTHONUTF8="1"
   python -m app.ingestion.ingest
   ```
   *(This step takes a few minutes as it communicates with Gmail, reads files, and passes all documents to Ollama for embedding generation).*

### Step 3: Verify the Data
To verify that payloads are successfully indexed with the unified metadata structures, use the verification script.
```powershell
# Windows PowerShell
$env:PYTHONUTF8="1"
python verify_payloads.py
```
*Expected Output: Should show a green `✅` status with 60+ chunks and the `subject` and `date_ts` fields successfully located under the metadata keys.*

### Step 4: Start the Backend API
Start the FastAPI server as usual to serve RAG requests.
```powershell
# Windows PowerShell
cd D:\PROJECTS\GenAI\EchoMind\backend
uvicorn app.main:app --reload
```
