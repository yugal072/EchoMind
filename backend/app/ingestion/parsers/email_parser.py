import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "connectors"))

from gmails import list_recent_emails


BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "data" / "parsed" / "emails"
OUT.mkdir(parents=True, exist_ok=True)


def parse_emails(max_results=10):
    parsed = []
    for email in list_recent_emails(max_results):
        text = (email.get("body") or email.get("snippet") or "").strip()
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
