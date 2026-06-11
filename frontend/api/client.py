# Moving from fastapi to cloud deployment, this client will be used to interact with the backend API.  loaclhost:8000 ----> aws

import requests
BASE_URL = "http://localhost:8000"  # Change this to your AWS endpoint when deployed

def ingest():
    response = requests.post(f"{BASE_URL}/ingest")
    return response.json()

def chat(question, session_id):
    response = requests.post(f"{BASE_URL}/chat",
                             json = {"question": question, "session_id": session_id
                                     }
                             )
    return response.json()


