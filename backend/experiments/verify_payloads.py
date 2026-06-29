"""
Verification script: scroll the Qdrant collection and confirm that
date_ts + subject are present on stored payloads.

Run AFTER:
  1. qdrant.exe is started (http://localhost:6333)
  2. python -m app.ingestion.ingest   has completed

Usage (from d:\PROJECTS\GenAI\EchoMind\backend):
    python verify_payloads.py
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv(r"D:\PROJECTS\GenAI\EchoMind\.env")

host = os.getenv("QDRANT_HOST", "localhost")
port = int(os.getenv("QDRANT_PORT", 6333))
collection = os.getenv("QDRANT_COLLECTION_NAME", "echomind_documents")

client = QdrantClient(url=f"http://{host}:{port}")

info = client.get_collection(collection)
print(f"\n📦 Collection: {collection}")
print(f"   Points count : {info.points_count}")
print(f"   Status       : {info.status}\n")

# Scroll the first 20 points and check payload fields
scroll_result, _ = client.scroll(
    collection_name=collection,
    limit=20,
    with_payload=True,
    with_vectors=False,
)

if not scroll_result:
    print("⚠️  Collection is empty — run ingestion first.")
else:
    # Group by source and check for required fields
    from collections import defaultdict
    by_source = defaultdict(list)
    for point in scroll_result:
        # LangChain nests document metadata inside a "metadata" dict in the Qdrant payload
        meta = point.payload.get("metadata", {})
        src = meta.get("source", "unknown")
        by_source[src].append(meta)

    REQUIRED_FIELDS = {"source", "subject", "date_ts"}

    for source, payloads in sorted(by_source.items()):
        sample = payloads[0]
        missing = REQUIRED_FIELDS - set(sample.keys())
        status = "✅" if not missing else f"❌ MISSING: {missing}"
        print(f"  source={source!r:12}  count={len(payloads)}  {status}")
        print(f"    sample keys: {sorted(sample.keys())}")
        print(f"    subject  : {sample.get('subject', '<not set>')!r}")
        print(f"    date_ts  : {sample.get('date_ts', '<not set>')}")
        print()

# Also demonstrate a filtered query
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

print("— Filtered query test: source == 'gmail' —")
result, _ = client.scroll(
    collection_name=collection,
    scroll_filter=Filter(must=[
        FieldCondition(key="metadata.source", match=MatchValue(value="gmail"))
    ]),
    limit=5,
    with_payload=True,
    with_vectors=False,
)
if result:
    for p in result:
        meta = p.payload.get('metadata', {})
        print(f"  ✅ id={p.id}  subject={meta.get('subject','?')!r}  date_ts={meta.get('date_ts','?')}")
else:
    print("  (no gmail documents found — ingest emails first)")
