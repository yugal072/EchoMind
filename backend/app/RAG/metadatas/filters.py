from typing import Optional, Dict
def build_metadata_filter(
    source: Optional[str] = None,
    sender: Optional[str] = None,
    subject: Optional[str] = None,
    date_after: Optional[str] = None,
    date_before: Optional[str] = None,
    document_type: Optional[str] = None,
) -> Optional[Dict]:
    """
    Builds a Chroma-compatible metadata filter dict.
    All incoming values must be plain strings by this point.
    Returns None if no valid filters are present.
    """
    conditions = []

    if source:
        conditions.append({"source": {"$eq": source}})

    if sender:
        # Use $contains for partial match (e.g. "placement" matches "placement@college.edu")
        conditions.append({"sender": {"$eq": sender}})

    if subject:
        conditions.append({"subject": {"$eq": subject}})  #   -- not supported by chroma (later change to $contains for QDRANT)

    if date_after:
        conditions.append({"date": {"$gte": date_after}})

    if date_before:
        conditions.append({"date": {"$lte": date_before}})

    if document_type:
        conditions.append({"document_type": {"$eq": document_type}})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]

    return {"$and": conditions}