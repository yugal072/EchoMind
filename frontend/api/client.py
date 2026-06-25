# Moving from fastapi to cloud deployment, this client will be used to interact with the backend API.  loaclhost:8000 ----> aws

import requests
from pathlib import Path
BASE_URL = "http://localhost:8000"  # Change this to your AWS endpoint when deployed

def upload(file_paths):
    files_payload = []
    
    for path in file_paths:
        if isinstance(path, str):
            path= Path(path)
        with open(path, 'rb') as f:
            files_payload.append(
                ("files",(path.name, f.read(), "application/octet-stream"))
            )
    response = requests.post(f"{BASE_URL}/upload", files=files_payload)
    return response.json()

def ingest():
    response = requests.post(f"{BASE_URL}/ingest")
    return response.json()

def ingest_audio(file_path: str):
    response = requests.post(
        f"{BASE_URL}/ingest/audio",
        json={"file_path": file_path}
    )
    return response


def chat(question, session_id):
    response = requests.post(f"{BASE_URL}/chat",
                             json = {"question": question, "session_id": session_id
                                     }
                             )
    return response.json()


