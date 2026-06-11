import base64
import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CONNECTOR_DIR = Path(__file__).resolve().parent
TOKEN_PATH = CONNECTOR_DIR / "token.json"
CREDS_PATH = CONNECTOR_DIR / "credentials.json"


def _get_header(headers, name):
    return next((h["value"] for h in headers if h["name"].lower() == name.lower()), "")


def _get_body(payload):
    if payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        text = _get_body(part)
        if text:
            return text

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


def list_recent_emails(max_results=10):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()
        headers = msg_data["payload"]["headers"]
        emails.append({
            "id": msg["id"],
            "subject": _get_header(headers, "Subject") or "No Subject",
            "from": _get_header(headers, "From"),
            "date": _get_header(headers, "Date"),
            "snippet": msg_data.get("snippet", ""),
            "body": _get_body(msg_data["payload"]),
        })
    return emails


if __name__ == "__main__":
    emails = list_recent_emails(1)
    print("SUBJECT:", emails[0]["subject"])
    print("BODY:")
    print(emails[0]["body"][:1000])