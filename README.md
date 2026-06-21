# EchoMind

> **A completely private agentic personal knowledge operating system.**  
> EchoMind automatically reads and organizes your emails, notes, and PDFs, storing them in a local vectorstore. Users can query their knowledge base, and the RAG pipeline responds with the most accurate and contextually relevant information.


![Status](https://img.shields.io/badge/Status-MVP%20In%20Progress-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-orange)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Technologies Used](#technologies-used)
- [Evaluation](#evaluation)
- [Screenshots](#screenshots)
- [License](#license)

---

## Overview

EchoMind is a privacy-first, local-first personal knowledge management system that ingests data from multiple sources—emails, PDFs, and text files—and enables intelligent, conversational retrieval through a RAG (Retrieval-Augmented Generation) pipeline. Designed with modularity and extensibility in mind, it allows users to upload documents, filter by metadata, and maintain session history across conversations.

---

## ✨ Features

- **Multi-source ingestion** – Gmail, PDFs, and `.txt` files  
- **Intelligent parsing** – Uses LlamaParse for PDF processing  
- **Hybrid RAG pipeline** – Combines semantic search with metadata filtering (source, date, sender, subject, etc.)  
- **Multi-turn conversational memory** – Persistent chat history across sessions  
- **Metadata filtering** – Filter queries by document type, sender, date, and more  
- **FastAPI backend** – RESTful API for scalable integration  
- **Streamlit UI** – Simple and interactive frontend for prototyping  
- **Built-in Evaluation Harness** – RAGAS-based metrics for system performance assessment  
- **Local-first & Privacy-focused** – All data stays on your machine

---

## Workflow

### 1. Data Ingestion

- **Sources**: Emails (Gmail API), PDFs, and text files  
- **Processing**:
  - Emails are fetched using credentials from `credentials.json` and converted from HTML to plain text  
  - PDFs are parsed using `PyMuPDFReader`; metadata is extracted  
  - Text files are read directly  
- **Deduplication**: Each file is assigned a unique ID (`file_{filename}_{content_hash}`) using `hashlib` to prevent duplicates in the vectorstore  
- **Storage**: Files are stored in a structured table with metadata for future retrieval

### 2. File Upload

- Users can upload documents directly via the Streamlit UI  
- The `/upload` endpoint handles parsing, hash generation, and vectorstore insertion  
- Uploaded files follow the same ingestion pipeline to ensure consistency

### 3. RAG Pipeline

Located in `RAG/index.py`, the pipeline includes:

- **Vectorstore**: ChromaDB (MVP) – planned migration to Qdrant and GraphDB  
- **Embeddings**: NvidiaEmbeddings for fast, cloud-based vectorization  
- **LLM**: Groq's `meta-llama/llama-4-scout-17b-16e-instruct` for efficient response generation  
- **Retrieval**: Supports metadata-based filtering (source, sender, subject, date range, etc.)  
- **Filter extraction**: A supplementary chain extracts filters directly from user queries

### 4. Metadata Filtering

- Metadata fields: `source`, `sender`, `subject`, `date_after`, `date_before`, `document_type`  
- String and datetime filters are currently limited due to ChromaDB constraints, but will be expanded with future Qdrant/GraphDB integration  
- A custom `extract_filters()` function combines manual and LLM-extracted filters before query execution

### 5. Session Persistency

- **Temporary chat history** initially used Langchain's `MessageHistory`  
- **Persistent session management** was implemented using:
  - `PersistenceSessionStore` – handles saving/loading session data to/from `./storage`  
  - `PersistentChatMessageHistory` – extends `ChatMessageHistory` to automate persistent storage  
- Sessions are integrated into the RAG chain via `RunnableWithMessageHistory()`

### 6. Frontend

- Built with **Streamlit** for rapid prototyping  
- Communicates with the FastAPI backend on port `8000`  
- Frontend and backend run separately

---

## Project Structure

```
EchoMind/
├── backend/
│   ├── app/
│   │   ├── core/              # Configuration and settings
│   │   ├── ingestion/         # Connectors and data pipelines
│   │   ├── RAG/               # Indexing, retrieval, and filtering
│   │   ├── eval/              # Evaluation harness (RAGAS)
│   │   └── main.py            # FastAPI application entrypoint
│   └── data/                  # Vectorstore and parsed files
├── frontend/                  # Streamlit UI
├── docs/                      # Documentation
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Nvidia API Key](https://build.nvidia.com/)
- [Groq API Key](https://console.groq.com/)
- [LlamaParse API Key](https://cloud.llamaindex.ai/)

### Installation

```bash
# Clone the repository
git clone https://github.com/yugal072/EchoMind.git
cd EchoMind

# Create and activate Conda environment
conda create -n echomind python=3.11
conda activate echomind

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
# Terminal 1: Backend
cd backend/
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend/
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501` (frontend) and `http://localhost:8000` (backend API).

---

## Technologies Used

- **Language**: Python 3.11  
- **Backend**: FastAPI, Uvicorn  
- **Frontend**: Streamlit  
- **Vector Database**: ChromaDB (current), future plans for Qdrant and GraphDB  
- **Embeddings**: NvidiaEmbeddings  
- **LLM**: Groq (`meta-llama/llama-4-scout-17b-16e-instruct`)  
- **Evaluation Framework**: RAGAS  
- **Document Parsing**: PyMuPDFReader, LlamaParse  
- **Email Integration**: Gmail API  

---

## Evaluation

The system includes a built-in evaluation harness to measure performance:

- **Dataset**: Custom dataset of Q&A pairs based on ingested content  
- **Runner**: `runner.py` executes queries and records outputs  
- **Metrics** (via `ragas_metrics.py`):
  - **Faithfulness** – Is the response grounded in the retrieved context?  
  - **Answer Relevancy** – Is the response relevant to the query?  
  - **Context Precision** – How precise is the retrieved context?  
  - **Context Recall** – Does the retrieved context cover all necessary information?  
- **Reporting**: Results are saved as a JSON file with per-metric scores

---

## 📸 Screenshots

*(Add screenshots of your application here)*

---

## 📄 License

*(Add your license information here)*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/yugal072/EchoMind/issues) for open tasks.

---

## 📬 Contact

- **Author**: Yugal  
- **GitHub**: [yugal072](https://github.com/yugal072)  
- **Project Link**: [https://github.com/yugal072/EchoMind](https://github.com/yugal072/EchoMind)

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Streamlit](https://streamlit.io/)  
- [Groq](https://groq.com/)  
- [Nvidia](https://build.nvidia.com/)  
- [LlamaIndex](https://www.llamaindex.ai/)