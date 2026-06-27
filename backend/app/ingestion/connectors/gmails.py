import base64
import os.path
from datetime import datetime
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.core.config import EMAIL_DIR, BASE_DIR
from app.ingestion.loaders.email_tracker import save_ingested_ids, load_ingested_ids

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CONNECTOR_DIR = Path(__file__).resolve().parent
TOKEN_PATH = CONNECTOR_DIR / "gmail_token.json"
CREDS_PATH = CONNECTOR_DIR / "credentials.json"


def _get_header(headers, name):
    return next((h["value"] for h in headers if h["name"].lower() == name.lower()), "")


def _get_body(payload):
    # First search for text/plain
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            
    for part in payload.get("parts", []):
        text = _get_body(part)
        if text:
            return text

    if payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    
    return ""


def get_gmail_service():
    if not CREDS_PATH.exists() and not TOKEN_PATH.exists():
        raise FileNotFoundError(
            f"Gmail credentials not found. Download OAuth credentials from Google Cloud Console "
            f"and save as:\n  {CREDS_PATH}"
        )

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes=SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS_PATH.exists():
                raise FileNotFoundError(
                    f"Gmail token missing or expired. Place credentials.json at:\n  {CREDS_PATH}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def list_recent_emails(max_results=20):
    """ Fetch recent emails but skip the existing ones"""
    service = get_gmail_service()
    
    ingested_ids = load_ingested_ids()
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    new_ids = set()
    for msg in messages:
        email_id = msg['id']
        
        if email_id in ingested_ids:
            continue
        
        msg_data = service.users().messages().get(
            userId="me", id=email_id, format="full"
        ).execute()
        
        headers = msg_data["payload"]["headers"]
        email = {
            "source": "gmail",
            "id": msg["id"],
            "subject": _get_header(headers, "Subject") or "No Subject",
            "from": _get_header(headers, "From"),
            "date": _get_header(headers, "Date"),
            "snippet": msg_data.get("snippet", ""),
            "raw_data": msg_data,
            "body": _get_body(msg_data["payload"]),
        }
        
        save_raw_emails(email)
        emails.append(email)
        new_ids.add(email_id)
        
    if new_ids:
        ingested_ids.update(new_ids)
        save_ingested_ids(ingested_ids)
    
    print(f"Fetched {len(emails)} new emails (skipped {len(messages) - len(emails)} already ingested)")
    return emails
    

def save_raw_emails(email:dict):
    """save raw email as json"""
    # create date based data folder if it doesnt exist
    try:
        email_date = email.get('date','')
        if email_date:
            date_str = email_date.split(',')[1].strip()[:11]  # rough parse
            folder_name = datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
        else:
            folder_name = "unknown date"
        
    except:
        folder_name = "unknown date"
        
    raw_dir = BASE_DIR/ "data" / "uploads" / "emails"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = raw_dir/ f"{email['id']}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(email, f, indent=2, ensure_ascii=False)
    

if __name__ == "__main__":
    emails = list_recent_emails(5)
    print(f"Fetched {len(emails)} new emails")
    if emails:
        print("SUBJECT:", emails[0]["subject"])
        print("BODY:", emails[0]["body"][:500])
    else:
        print("No new emails to show.")