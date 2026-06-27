from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DUMPS_DIR = DATA_DIR / "dumps"

UPLOAD_DIR = DATA_DIR / "uploads"

FILES_DIR = UPLOAD_DIR / "files"

CALENDAR_DIR = UPLOAD_DIR / "calendar"

EMAIL_DIR = UPLOAD_DIR / "emails"

VECTORSTORE_DIR = DATA_DIR / "vectorstore"

APP_DIR = Path(__file__).resolve().parents[1]

SESSION_STORE_DIR = APP_DIR / "sessions" / "storage"