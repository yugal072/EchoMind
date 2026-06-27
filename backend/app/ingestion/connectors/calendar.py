import json
from datetime import datetime
from pathlib import Path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.core.config import CALENDAR_DIR
from app.ingestion.loaders.calendar_tracker import load_ingested_calendar_ids, save_ingested_calendar_ids

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CONNECTOR_DIR = Path(__file__).resolve().parent
TOKEN_PATH = CONNECTOR_DIR / "calendar_token.json"
CREDS_PATH = CONNECTOR_DIR / "credentials.json"



def get_calendar_service():
    if not CREDS_PATH.exists() and not TOKEN_PATH.exists():
        raise FileNotFoundError(
            f"Credentials not found. Download OAuth credentials from Google Cloud Console "
            f"and save as:\n  {CREDS_PATH}"
        )

    creds= None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes=SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_PATH.exists():
                raise FileNotFoundError(
                    f"Calendar token missing or expired. Place credentials.json at:\n  {CREDS_PATH}"
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
            
        TOKEN_PATH.write_text(creds.to_json())
        
    return build("calendar", "v3", credentials=creds)  # returning the service


def list_upcomming_events(max_result = 20):
    """Fetch the upcomming events from google calendar"""
    service = get_calendar_service()
    ingested_ids = load_ingested_calendar_ids("calendar")
    
    now = datetime.utcnow().isoformat() + "Z"    # RFC3339 format
    
    try:
        print("Getting the upcomming 20 events")
        
        event_results = service.events().list(
            calendarId = "primary",
            timeMin = now,
            maxResults = max_result,
            singleEvents = True,
            orderBy = "startTime"
        ).execute()
        
        events = event_results.get("items",[])
        new_events = []
        new_ids = set()
        
        for event in events:
            event_id = event['id']
            
            if event_id in ingested_ids:
                continue
            new_events.append(event)
            new_ids.add(event_id)
            
        if new_ids:
            ingested_ids.update(new_ids)
            save_ingested_calendar_ids("calendar", ingested_ids)
        
        print(f"Fetched {len(new_events)} new calendar events (skipped {len(events) - len(new_events)} already ingested)")
        return new_events
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    service = get_calendar_service()
    print("✅ Calendar service created successfully!")