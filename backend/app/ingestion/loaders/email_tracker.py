import json
from pathlib import Path

from app.core.config import BASE_DIR
TRACKER_FILE = BASE_DIR / "data" / "parsed" / "emails" / "ingested_ids.json"



def load_ingested_ids() -> set:
    if TRACKER_FILE.exists():
        try:
            data = json.loads(TRACKER_FILE.read_text(encoding="utf-8"))
            return set(data)
        except:
            return set()
    return set()


def save_ingested_ids(ids_set: set):
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids_set), f, indent=2)