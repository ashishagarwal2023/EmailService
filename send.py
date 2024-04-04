import base64
import os.path
import pickle
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send(to_list, subject, body):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    
    for to in to_list:
        b = body.replace("{email}", to)
        message = MIMEText(b, 'html')
        message['to'] = to
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        try:
            message = (service.users().messages().send(userId="me", body=create_message).execute())
        except HTTPError as error:
            print(f"Failed to send email to {to}")
        finally:
            print("Sent one email")