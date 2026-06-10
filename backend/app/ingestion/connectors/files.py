import numpy as np  
import glob
import json
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from app.core.config import DUMPS_DIR, VECTORSTORE_DIR



def read_txt_file()->str:
    data=""
    for filepath in glob.glob(f"{DUMPS_DIR}/*.txt"):
        with open(filepath, "r", encoding="utf-8") as file:
            data += file.read()
    return data



def read_pdf()->str:
    pdf_text=""
    for filepath in glob.glob(f"{DUMPS_DIR}/*.pdf"):
        loader = PyPDFLoader(filepath)
        texts = loader.load()
        for text in texts:
            pdf_text += text.page_content + "\n"
  
    return pdf_text




    
