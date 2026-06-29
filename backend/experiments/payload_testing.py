from app.RAG.index import get_vectorstore
from qdrant_client.http import models

vs = get_vectorstore()
client = vs.client
collection_name = vs.collection_name

text_fields = ["subject", "sender", "location"]
for field in text_fields:
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field,
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                lowercase=True,
            ),
        )
        print(f"✅ Created text index on '{field}'")
    except Exception as e:
        print(f"⚠️ Could not create index on '{field}': {e}")

numeric_fields = ["date_ts"]
for field in numeric_fields:
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field,
            field_schema=models.PayloadSchemaType.FLOAT,
        )
        print(f"✅ Created numeric index on '{field}'")
    except Exception as e:
        print(f"⚠️ Could not create index on '{field}': {e}")

keyword_fields = ["source", "document_type", "folder", "language"]
for field in keyword_fields:
    try:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field,
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        print(f"✅ Created keyword index on '{field}'")
    except Exception as e:
        print(f"⚠️ Could not create index on '{field}': {e}")

info = client.get_collection(collection_name)
print("Final payload schema:", info.payload_schema)