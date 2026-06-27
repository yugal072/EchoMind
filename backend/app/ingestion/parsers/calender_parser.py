from app.ingestion.connectors.calendar import list_upcomming_events
from datetime import datetime
from langchain_core.documents import Document


def parse_events(events):
    """Convert raw Google Calendar events into langchain Documents"""
    documents=[]
    
    if not events:
        print("No events to parse")
        return []
    
    for event in events:
        start = event['start'].get('dateTime') or event['start'].get('date')
        end = event['end'].get('dateTime') or event['end'].get('date')
        
        # Clean description
        description = event.get('description','') or ''
        
        content = f"""
        Event: {event.get('summary', 'No Title')} 
        Time: {start} to {end}
        Location: {event.get('location', 'No location')}       
        Description: {description}
        """.strip()
        
        doc = Document(
            page_content=content,
            metadata = {
                "source": "calendar",
                "event_id": event['id'],
                "summary": event.get('summary',''),
                "start": start,
                "end": end,
                "location": event.get('location', ''),
                "attendees": len(event.get('attendees',[])),
                "ingested_at": datetime.now().isoformat(),
            }
        )
        documents.append(doc)
        
    return documents