from groq import Groq
from pathlib import Path
from datetime import datetime
from typing import List
from langchain_core.documents import Document
from ..parsers.audio_parser import audio_parser

def load_audio_file(audio_path: str | Path)-> List[Document]:
    
    audio_path = Path(audio_path).resolve()
    print(f"DEBUG: Trying to open file: {audio_path}")
    
    if not audio_path.exists():
        print(f"FIle not found :{audio_path}")
        return []
    
    result= audio_parser.transcribe_audio(audio_path)
    
    # Handle error case when it returns string insead of dict
    if isinstance(result, str):
        print(f"Transcription failed: {result}")
        return []
    
    doc = Document(
        page_content=result['text'],
        metadata={
            "source": "audio",
            "filename": result['filename'],
            "subject": result['filename'],           # shared alias used by subject filter
            "file_path": result['file_path'],
            "language": result['language'],
            "duration": result['duration'],
            "ingested_at": datetime.now().isoformat(),
            "date_ts": datetime.now().timestamp(),   # ingestion time as Unix float (best available)
            "type": "voice note",
        }
    )
    
    return [doc]

def get_audio_documents(audio_dir: str = None, audio_files: List[str] = None) -> List[Document]:
    """
    Load multiple audio files from directory or list
    """
    documents = []
    
    if audio_files:
        paths = [Path(f) for f in audio_files]
    elif audio_dir:
        audio_dir = Path(audio_dir)
        paths = list(audio_dir.glob("**/*.*"))
        paths = [p for p in paths if p.suffix.lower() in [".mp3", ".wav", ".m4a", ".ogg"]]
    else:
        return []

    for path in paths:
        try:
            docs = load_audio_file(path)
            documents.extend(docs)
            print(f"✅ Transcribed: {path.name}")
        except Exception as e:
            print(f"❌ Failed to transcribe {path.name}: {e}")

    return documents


def test_single_audio_file():
    print("=== Testing Single Audio File ===")
    
    # Change this path to your actual file
    test_file = r"D:\PROJECTS\GenAI\EchoMind\backend\app\ingestion\connectors\sample-speech-1m.mp3"
    
    if not Path(test_file).exists():
        print(f"❌ File not found: {test_file}")
        return
    
    documents = load_audio_file(test_file)
    
    if documents:
        doc = documents[0]
        print(f"✅ Success! Created {len(documents)} document(s)")
        print(f"Filename: {doc.metadata['filename']}")
        print(f"Text length: {len(doc.page_content)} characters")
        print(f"First 150 chars:\n{doc.page_content[:150]}...")
    else:
        print("❌ Failed to create document")

# Trial/ Test
if __name__ == "__main__":
    result = test_single_audio_file()
    print(result)


