from typing import Optional, Dict
def build_metadata_filter(
    source: Optional[str] = None,
    #sender: Optional[str] = None,       # NOTE: not used for Chroma filter (no substring support)
    #subject: Optional[str] = None,      # NOTE: not used for Chroma filter (no substring support)
    date_after: Optional[str] = None,
    date_before: Optional[str] = None,
    document_type: Optional[str] = None,
) -> Optional[Dict]:
    
    and_conditions = []

    if source and str(source).strip():
        and_conditions.append({"source": {"$eq": str(source).strip()}})

    # sender and subject are intentionally NOT filtered via Chroma metadata:
    # - The 'from' field stores full RFC headers e.g. 'Name <email@domain.com>'
    # - The 'subject' field needs substring/contains matching which Chroma doesn't support
    # - Both fields are embedded in page_content, so semantic search handles them naturally

    if date_after and str(date_after).strip():
        and_conditions.append({"date": {"$gte": str(date_after).strip()}})

    if date_before and str(date_before).strip():
        and_conditions.append({"date": {"$lte": str(date_before).strip()}})

    if document_type and str(document_type).strip():
        and_conditions.append({"document_type": {"$eq": str(document_type).strip()}})

    if not and_conditions:
        return None
    if len(and_conditions) == 1:
        return and_conditions[0]
    return {"$and": and_conditions}