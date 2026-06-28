from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class FilterCondition:
    key: str
    op: str        # "eq", "match_text", "gte", "lte", "any"
    value: Any


@dataclass
class MetadataFilterSpec:
    conditions: List[FilterCondition] = field(default_factory=list)

    def is_empty(self) -> bool:
        return len(self.conditions) == 0


def build_metadata_filter(
    source: Optional[str] = None,
    sender: Optional[str] = None,
    subject: Optional[str] = None,
    date_after: Optional[str] = None,
    date_before: Optional[str] = None,
    document_type: Optional[str] = None,
    tags: Optional[str] = None,          # comma-separated tag string from LLM, e.g. "internship,placement"
    folder: Optional[str] = None,        # obsidian folder name
    language: Optional[str] = None,      # audio transcription language
    location: Optional[str] = None,      # calendar event location
) -> Optional[MetadataFilterSpec]:
    """
    Backend-agnostic metadata filter spec covering gmail, pdf, audio, calendar, and obsidian sources.
    Returns None if no valid filters are present.
    """
    conditions: List[FilterCondition] = []

    if source:
        conditions.append(FilterCondition(key="source", op="eq", value=source))

    if document_type:
        conditions.append(FilterCondition(key="document_type", op="eq", value=document_type))

    if sender:
        conditions.append(FilterCondition(key="sender", op="match_text", value=sender))

    if subject:
        # subject is aliased across sources (email subject, calendar summary, obsidian title)
        conditions.append(FilterCondition(key="subject", op="match_text", value=subject))

    if date_after:
        conditions.append(FilterCondition(key="date_ts", op="gte", value=date_after))

    if date_before:
        conditions.append(FilterCondition(key="date_ts", op="lte", value=date_before))

    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            conditions.append(FilterCondition(key="tags", op="any", value=tag_list))

    if folder:
        conditions.append(FilterCondition(key="folder", op="eq", value=folder))

    if language:
        conditions.append(FilterCondition(key="language", op="eq", value=language))

    if location:
        conditions.append(FilterCondition(key="location", op="match_text", value=location))

    if not conditions:
        return None

    return MetadataFilterSpec(conditions=conditions)