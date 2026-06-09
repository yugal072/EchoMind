import os
import requests
from dotenv import load_dotenv
load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = "1174326409093957"

url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "messaging_product": "whatsapp",
    "to": "91XXXXXXXXXX",
    "type": "text",
    "text": {
        "body": "Hello from Python"
    }
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print(response.json())