import json
import sys
import re
from bs4 import BeautifulSoup
from pathlib import Path

from app.core.config import BASE_DIR, DATA_DIR
from app.ingestion.connectors.gmails import list_recent_emails


OUT = BASE_DIR / "data" / "parsed" / "emails"
OUT.mkdir(parents=True, exist_ok=True)

INGESTED_TRACKER = OUT/"ingested_email_ids.json"

def load_ingested_ids():
    if INGESTED_TRACKER.exists():
        try:
            return set(json.loads(INGESTED_TRACKER.read_text(encoding="utf-8")))
        except:
            return set()
    return set()

def save_ingested_ids(ids_set:set):
    INGESTED_TRACKER.write_text(json.dumps(list(ids_set),indent=2), encoding= "utf-8")

def clean_html(html_content:str):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator="\n").strip()

def clean_email_text(text:str):
    if not text:
        return ""
    # remove urls
    text = re.sub(r"https?://\S+", "", text)
    
    # remove boilerplate
    patterns = [
        r"unsubscribe.*",  
        r"privacy.*",
        r"help.*",
        r"learn why we included this.*",
        r"all rights reserved.*",
        r"copyright.*",
        r"this email was intended for.*",
        r"view in browser.*",    
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags = re.IGNORECASE)
    # remove extra whitespace
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    return text
    
def parse_emails(max_results=10):
    ingested_ids = load_ingested_ids()
    parsed = []
    new_ids= set()
    
    for email in list_recent_emails(max_results):
        email_id = email['id']
        
        if email_id in ingested_ids:
            print(f"⏭️ Skipping already ingested email: {email.get('subject', '')[:60]}...")
            continue
        
        raw_text = email.get("body") or email.get("snippet") or ""
        text = clean_html(raw_text)
        text = clean_email_text(text)
        
        
        parsed.append({
            "id": email["id"],
            "subject": email.get("subject", ""),
            "from": email.get("from", ""),
            "date": email.get("date", ""),
            "text": text,
        })
        new_ids.add(email_id)
    
    if new_ids:
        ingested_ids.update(new_ids)
        save_ingested_ids(ingested_ids)
        print(f"Saved {len(new_ids)} new email IDs to tracker")
    return parsed


if __name__ == "__main__":
    try:
        emails = parse_emails(10)
    except FileNotFoundError as e:
        sys.exit(str(e))

    if not emails:
        sys.exit("No emails fetched. Check Gmail API access and inbox.")

    out_path = OUT / "emails.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)
    print(f"Parsed {len(emails)} emails -> {out_path}")
