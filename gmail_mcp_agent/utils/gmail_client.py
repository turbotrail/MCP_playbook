import os
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

class GmailClient:
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    
    def __init__(self):
        load_dotenv()
        self.credentials_file = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
        self.api_key = os.getenv('GMAIL_API_KEY')
        self.service = self._get_gmail_service()
    
    def _get_gmail_service(self):
        if self.api_key:
            return build('gmail', 'v1', developerKey=self.api_key)
        
        # Fallback to OAuth2 if no API key is provided
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def get_unread_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get unread emails from Gmail."""
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                
                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'snippet': msg['snippet']
                })
            
            return emails
        except Exception as e:
            if "API key" in str(e):
                print("Error: API key authentication is not sufficient for Gmail API operations.")
                print("Please use OAuth2 authentication instead.")
            raise e
    
    def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send an email using Gmail API."""
        try:
            message = {
                'raw': self._create_message(to, subject, body)
            }
            
            return self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
        except Exception as e:
            if "API key" in str(e):
                print("Error: API key authentication is not sufficient for sending emails.")
                print("Please use OAuth2 authentication instead.")
            raise e
    
    def _create_message(self, to: str, subject: str, body: str) -> str:
        """Create a base64 encoded email message."""
        import base64
        from email.mime.text import MIMEText
        
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        return base64.urlsafe_b64encode(message.as_bytes()).decode() 