# EchoMind
> A completely private agentic personal knowledge operating system. It automatically reads and organizes your emails, reads notes, pdfs and stores them in local vectorstore. The user inputs its query and the RAG pipeline replies with the most appropriate and accurate data based on the query and retrieved context. 

The Workflow is divided into:
1. Data Ingestion.
- The data is currently ingested into three formats- emails, pdfs, texts.
- The emails are fetched from the the the email api. The tokens and other credentials are extracted from "credentials.json" file. The emails are then further parsed from html format to pure text format. 
- The pdf and text files are read with the help of readers like 'PyMuPDFReader' and then pdfs are parsed of their metadata.
- The parsed content from emails, pdfs along with the data extracted from .txt files are then loaded with formated metadata.
- On next step each file is then given a unique id/name with the help of its type, filename and a unique hash code created with the help of hashlib. The file id is then in the format "file_{filename}_{content_hash}"
- At last the files are stored in the form of table with a file_id representing the particular file to prevent the duplication of the files in the vectorstore.


2. Uploading files
- This feature allows user to diercly upload files from the streamilt UI and store it into the vectorstore
- In @app.post("/upload") upload_loder manages the uploading and parsing of the uploaded documents just the way which happens in the ingestion method.
- Then the vector_ingestion handles the hash id generations and assigning them to the uploaded file and then finally upload the file into the vectorstore.

3. RAG Pipeline
- The RAG/index.py contains the code for entire RAG pipeline from getting vectorstore to invoking the the RAG chain to the user query.
- Functions listed inside the file goes by the list:
    - get_vectorstore()
    - get_retriever()
    - get_session_history()
    - get_rag_chain()
    - extract_filters()
    - ask() 
- All the documents and emails are saved into the chromadb till MVP. Will be later shifted to Qdrant and GraphDB for advanced data management and retrieving.
- The embedding model used is NvidiaEmbeddings which provide fast and robust cloud based embedding model.
- The llm model used in the chain is Groq's "meta-llama/llama-4-scout-17b-16e-instruct" which complies with the quick and efficient response retrieving model necessity guided by the system prompt given to the chain.

4. Evaluation Harness
- For evaluation a test dataset was created consisting a list of dicitonaries of questions and answers written based on the system prompt format.
- The runner.py file then extracts the questions from the dataset and queries it into the RAG pipeline and records the output.
- A new result json file is created consisting of output along with the context.
- Finally ragas_metrics.py file:
    - Creates a evaluator llm with seperating evaluator embeddings to evaluate the original vs required response to each question.
    - The llm is wrapped with the help of LangchainLLMWrapper.
    - The 'eavaluate()' function is run on the dataset for metrics - Faithfulness, Answer Relevancy, Context Precision, Context Recall.
    - Atlast save_report() returns a .json file consisting of the scores for each metrics. 

5. Metadata Filtering
- The metadata filtering is complying with Langchain retrieval metadata filtering.
- The metadatas are divided into categories- source, sender, subject, date_after, date_before, document_type.
- Due to Chroma limitations some string(subject) and datetime filters are kept on hold to implement them later with Qdrant and GraphDB integration.  
- Another method for filter extraction was implemented for the ease of useer.
- A filter extraction prompt was fed to a supplementary chain which extracts the filters directly from the user input question.
- Then in ask() function these manual and extracted filters are then combined and fed to the RAG invoke function. 

6. Session Persistency
- Intially only temporary chat history was added from langchain's MessageHistory which was not able to save and maintain the history of previous sessions.
- Therefore a new manual session history functionality was created for managing and storing session history into ./storage folder.
- The session_store.py function declares the Basemodel class structure for ChatMessage and SessionData. It also creates the class PersistenceSessionStore which contains functions to get_session_history() and store_session_history.
- A new class 'PersistentChatMessageHistory(ChatMessageHistory)' was created which inherits the ChatMessageHistory from langchain, to automate the process of getting and storing the session data.
- It inherits the get and store functions from parent class 'PersistenceSessionStore' and calls it.
- It then modifies the add_message() which is the inbuilt ChatMessageHistory function to take input and store according to the store_session_history() inside the parent class.
- After that inside get_session_history() function the class 'PersistentChatMessageHistory(ChatMessageHistory)' is called.
- The function get_message_history() is then fed to the RunnableWithMessageHistory() inside get_rag_chain() as a parameter under the same name.



---

## ✨ Features

- Multi-source ingestion (Gmail, PDFs, Text files)
- Intelligent parsing with LlamaParse
- Hybrid RAG with metadata filtering (source, date, sender, subject, etc.)
- Multi-turn conversational memory
- FastAPI backend + Streamlit UI
- Built-in Evaluation Harness (RAGAS)
- Local-first & Privacy-focused

---

## Project Structure
EchoMind/
├── backend/
│   ├── app/
│   │   ├── core/              # config, settings
│   │   ├── ingestion/         # connectors & pipeline
│   │   ├── RAG/               # index, retriever, filters
│   │   ├── eval/              # evaluation harness
│   │   └── main.py            # FastAPI endpoints
│   └── data/                  # vectorstore, parsed files
├── frontend/                  # Streamlit UI
├── docs/                      # documentation
├── .env.example
├── requirements.txt
└── README.md


## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Nvidia API Key
- Groq API Key
- LlamaParse API Key (for PDFs)

### Installation

```bash
# 1. Clone the repository
git clone <https://github.com/yugal072/EchoMind.git>
cd EchoMind

# 2. Create and activate environment
conda create -n echomind python=3.11
conda activate echomind

# 3. Install dependencies
pip install -r requirements.txt

#  4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

# Running the APplication
```bash
# Terminal 1
cd backend/
uvicorn app.main:app --reload 

# Terminal 2
cd frontend/
streamlit run streamlit_app.py