from app.ingestion.connectors.calendar import list_upcomming_events
from datetime import datetime, timezone
from langchain_core.documents import Document


def parse_events(events):
    """Convert raw Google Calendar events into langchain Documents"""
    documents = []

    if not events:
        print("No events to parse")
        return []

    for event in events:
        start = event['start'].get('dateTime') or event['start'].get('date')
        end = event['end'].get('dateTime') or event['end'].get('date')

        # Clean description
        description = event.get('description', '') or ''

        content = f"""
        Event: {event.get('summary', 'No Title')}
        Time: {start} to {end}
        Location: {event.get('location', 'No location')}
        Description: {description}
        """.strip()

        # Parse start datetime to a Unix timestamp for date range filtering.
        # Google Calendar gives either "2026-07-01T10:00:00+05:30" (dateTime)
        # or "2026-07-01" (all-day date). Handle both formats.
        date_ts = None
        if start:
            try:
                # Full ISO datetime (with or without timezone offset)
                dt = datetime.fromisoformat(start)
                date_ts = dt.timestamp()
            except ValueError:
                try:
                    # Fallback: date-only string — treat as midnight UTC
                    date_ts = datetime.strptime(start, "%Y-%m-%d").replace(
                        tzinfo=timezone.utc
                    ).timestamp()
                except ValueError:
                    pass

        doc = Document(
            page_content=content,
            metadata={
                "source": "calendar",
                "event_id": event['id'],
                "summary": event.get('summary', ''),
                "subject": event.get('summary', ''),  # shared alias used by subject filter
                "start": start,
                "end": end,
                "date_ts": date_ts,                    # Unix float for date_after/date_before filters
                "location": event.get('location', ''),
                "attendees": len(event.get('attendees', [])),
                "ingested_at": datetime.now().isoformat(),
            }
        )
        documents.append(doc)

    return documents