import json
from pathlib import Path

from app.core.config import BASE_DIR

TRACKER_DIR = BASE_DIR / "data" / "parsed" / "calendar" 
TRACKER_DIR.mkdir(parents=True, exist_ok=True)


def get_tracker_path(source: str) -> Path:
    """Return the tracker file path"""             # just one file
    return TRACKER_DIR / f"{source}_ingested_ids.json"

def load_ingested_calendar_ids(source: str = "calendar")->set:
    """Load already ingested tracker Ids for a source"""
    tracker_path = get_tracker_path(source)
    
    if tracker_path.exists():
        try:
            data = json.loads(tracker_path.read_text(encoding = "utf-8"))
            return set(data)
        except Exception:
            return set()
        
    return set()

def save_ingested_calendar_ids(source: str, ingested_ids: set):
    """Save ingested IDs to tracker file"""
    tracker_path = get_tracker_path(source)
    
    try:
        tracker_path.write_text(
            json.dumps(list(ingested_ids), indent=2, ensure_ascii=False)
        )
    except Exception as e:
        print(f"Warning : could not save tracker for {source}: {e}")
        
        
        
if __name__ == "__main__":
    ids = load_ingested_calendar_ids("calendar")
    print(f"Loaded {len(ids)} ingested calendar event IDs")