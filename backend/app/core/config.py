from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

FILES_DIR = DATA_DIR / "files"

DUMPS_DIR = FILES_DIR / "dumps"

VECTORSTORE_DIR = DATA_DIR / "vectorstore"