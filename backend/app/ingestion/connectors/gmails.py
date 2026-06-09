import os.path 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open ("token.json","w") as token:
            token.write(creds.to_json())
            
    return build("gmail","v1", credentials=creds)


def list_recent_emails(max_results = 10):
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId = 'me', maxResults = max_results).execute()
        messages = results.get('messages',[])
        
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId = 'me', id = msg['id'], format = 'full').execute()
            emails.append({
                'id':msg['id'],
                'snippet':msg_data.get('snippet'),
                'subject': next((h['value'] for h in msg_data['payload']['headers'] if h['name'] == 'Subject'), 'No Subject')
                # can add date, body, attachments too
            
            })  
        return emails
    except Exception as e:
        print(f"An error eccored: {e}" )
        return []
    
if __name__ == "__main__":
    email = list_recent_emails(5)
    for emails in email:
        print(email)