# Converts the spec into a real Qdrant filter

from datetime import datetime
from typing import Optional
from qdrant_client.http import models
from app.RAG.metadatas.filters import MetadataFilterSpec


def _resolve_date(value: str) -> Optional[float]:
    """Convert a date string (ISO or fuzzy) into a Unix timestamp (float) for numeric range filtering."""
    v = value.lower().strip()
    today = datetime.utcnow()

    from datetime import timedelta
    fuzzy_map = {
        "today": today,
        "now": today,
        "recent": today - timedelta(days=7),
        "latest": today - timedelta(days=7),
        "last week": today - timedelta(days=7),
        "this week": today - timedelta(days=7),
    }
    if v in fuzzy_map:
        return fuzzy_map[v].timestamp()

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).timestamp()
        except ValueError:
            continue

    print(f"⚠️ Could not resolve date value '{value}', dropping date filter.")
    return None


def to_qdrant_filter(spec: Optional[MetadataFilterSpec]) -> Optional[models.Filter]:
    """Translates a backend-agnostic MetadataFilterSpec into a real qdrant_client Filter object."""
    if spec is None or spec.is_empty():
        return None

    must_conditions = []

    for cond in spec.conditions:
        # LangChain nests metadata under the 'metadata' key in the Qdrant payload
        qdrant_key = f"metadata.{cond.key}"

        if cond.op == "eq":
            must_conditions.append(
                models.FieldCondition(key=qdrant_key, match=models.MatchValue(value=cond.value))
            )

        elif cond.op == "match_text":
            # Full-text / substring-style match — requires the field to have a text index
            must_conditions.append(
                models.FieldCondition(key=qdrant_key, match=models.MatchText(text=cond.value))
            )

        elif cond.op in ("gte", "lte"):
            ts = _resolve_date(cond.value)
            if ts is None:
                continue   # skip unresolvable dates rather than crashing
            range_kwargs = {"gte": ts} if cond.op == "gte" else {"lte": ts}
            must_conditions.append(
                models.FieldCondition(key=qdrant_key, range=models.Range(**range_kwargs))
            )

        elif cond.op == "in":
            must_conditions.append(
                models.FieldCondition(key=qdrant_key, match=models.MatchAny(any=cond.value))
            )
        
        elif cond.op == "any":
            must_conditions.append(
                models.FieldCondition(key=qdrant_key, match=models.MatchAny(any=cond.value))
            )

    if not must_conditions:
        return None

    return models.Filter(must=must_conditions)