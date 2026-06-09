import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_parse import LlamaParse

# Project root: backend/app/ingestion/parsers -> EchoMind/
PROJECT_ROOT = Path(__file__).resolve().parents[4]
load_dotenv(PROJECT_ROOT / ".env")

BASE = Path(__file__).resolve().parents[3]  # backend/
DUMPS = BASE / "data" / "files" / "dumps"
OUT = BASE / "data" / "parsed" / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)

api_key = os.getenv("LLAMA_CLOUD_API_KEY") or os.getenv("LLAMA_PARSER_API_KEY")
base_url = os.getenv("LLAMA_CLOUD_BASE_URL")

def parse_pdfs():

    if not api_key:
        sys.exit(
            "Missing API key. Set LLAMA_CLOUD_API_KEY (or LLAMA_PARSER_API_KEY) in .env at project root."
        )

    parser_kwargs = {
        "api_key": api_key,
        "result_type": "markdown",
        "verbose": True,
        "ignore_errors": False,
    }
    if base_url:
        parser_kwargs["base_url"] = base_url

    parser = LlamaParse(**parser_kwargs)

    pdf_paths = [str(p) for p in DUMPS.glob("*.pdf")]
    if not pdf_paths:
        sys.exit(f"No PDF files found in {DUMPS}")

    print(f"Parsing {len(pdf_paths)} file(s)...")
    documents = parser.load_data(pdf_paths)

    if not documents:
        sys.exit(
            "Parser returned no documents. Check your API key and region "
            "(set LLAMA_CLOUD_BASE_URL=https://api.cloud.eu.llamaindex.ai for EU accounts)."
        )

    output = [{"text": d.text, "metadata": d.metadata} for d in documents]
    out_path = OUT / "llama_parser.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(output)} document(s) to {out_path}")

    return output