import json
import sys
from bs4 import BeautifulSoup

from app.core.config import BASE_DIR, DATA_DIR
from app.ingestion.connectors.gmails import list_recent_emails


OUT = BASE_DIR / "data" / "parsed" / "emails"
OUT.mkdir(parents=True, exist_ok=True)

def clean_html(html_content:str):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html_parser")
    
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator="\n").strip()
    
def parse_emails(max_results=10):
    parsed = []
    for email in list_recent_emails(max_results):
        raw_text = email.get("body") or email.get("snippet") or ""
        text = clean_html(raw_text)

        parsed.append({
            "id": email["id"],
            "subject": email.get("subject", ""),
            "from": email.get("from", ""),
            "date": email.get("date", ""),
            "text": text,
        })
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
