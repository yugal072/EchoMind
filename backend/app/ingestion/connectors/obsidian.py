from pathlib import Path
import os
import os.path
from typing import Optional, List
from langchain_core.documents import Document

from app.ingestion.parsers.obsidian_parser import parse_obsidian_file
from app.ingestion.pipeline import generate_uuid_from_string

def list_markdown_files(vault_path: str, subfolders: Optional[List[str]]= None)->List[str]:
    '''Recursively list all the .md files in the vault'''
    all_files = []
    vault_path= Path(vault_path)
    
    if not vault_path.is_dir():
        return []
    
    
    for root, dirs, files in os.walk(vault_path):
        # filter subfolders if specified
        if subfolders:
            dirs[:]= [d for d in dirs if d in subfolders]
            
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.join(root, file)
                all_files.append(full_path)
                    
    return all_files

def ingest_obsidian_vault(vault_path: str, subfolders: Optional[List[str]]= None)-> List[Document]:
    '''Ingest an obsidian vault into Documents format'''
    documents = []
    md_files = list_markdown_files(vault_path, subfolders)
    
    print(f"Found {len(md_files)} markdown files in vault.")
    
    for file_path in md_files:
        try:
            doc = parse_obsidian_file(file_path)
            if doc:
                documents.append(doc)
        except Exception as e:
            print(f"Failed to parse {file_path}: {e}")
            continue
        
    print(f"✅ Parsed {len(documents)} documents from Obsidian vault")
    return documents