import numpy as np  
import glob
import json
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path



def read_txt_file()->str:
    data=""
    for filepath in glob.glob("../../../data/files/dumps/*.txt"):
        with open(filepath, "r", encoding="utf-8") as file:
            data += file.read()
    return data



def read_pdf()->str:
    pdf_text=""
    for filepath in glob.glob("../../../data/files/dumps/*.pdf"):
        loader = PyPDFLoader(filepath)
        texts = loader.load()
        for text in texts:
            pdf_text += text.page_content + "\n"
  
    return pdf_text




    
