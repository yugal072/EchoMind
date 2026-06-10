# Run the Ingestion file everytime the new data is added or updated 
 
from pipeline import run_ingestion, split_documents
from RAG.index import get_vectorstore

def build_index():
    """ Run this only when new data is added"""
    print("Starting Ingestion")
    documents = run_ingestion()
    chunks = split_documents(documents)
    
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    print(f"✅ Added {len(chunks)} chunks to vectorstore")
    
if __name__ == "__main__":
    build_index()