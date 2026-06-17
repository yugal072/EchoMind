# Run the Ingestion file everytime the new data is added or updated 
 
from app.ingestion.pipeline import (
                                    split_documents,
                                    load_email_documents,
                                    load_file_documents,
                                    load_pdf_documents,
                                    get_email_ids,
                                    get_file_ids,
                                    get_pdf_ids)
from app.RAG.index import get_vectorstore

    
        
    

def build_index():
    """ Run this only when new data is added"""
    print("Starting Ingestion")
    try:
        pdf_documents = load_pdf_documents()
        pdf_chunks = split_documents(pdf_documents)
        pdf_ids = get_pdf_ids(chunks=pdf_chunks)
        
        email_documents = load_email_documents()
        email_chunks = split_documents(email_documents)
        email_ids = get_email_ids(email_chunks)
        
        file_documents = load_file_documents()
        file_chunks = split_documents(file_documents)
        file_ids = get_file_ids(file_chunks)
               
        vectorstore = get_vectorstore()
        
        if pdf_chunks:
            vectorstore.add_documents(documents=pdf_chunks, ids = pdf_ids)
        if email_chunks:
            vectorstore.add_documents(documents=email_chunks, ids= email_ids)
        if file_chunks:
            vectorstore.add_documents(documents=file_chunks, ids = file_ids)
        
        total= len(pdf_chunks)+ len(email_chunks) + len(file_chunks)
        total_chunks = vectorstore._collection.count()
        
        print(f"✅ Added {total} chunks to vectorstore")
        print(f"✅ Total chunks in vectorstore now: {total_chunks}")
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        raise


    
if __name__ == "__main__":
    build_index()