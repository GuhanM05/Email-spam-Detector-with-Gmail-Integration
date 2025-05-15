
import os
import pickle
import time
import base64
from email import message_from_bytes
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import your prediction function
from rf_predict import predict_rf

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_recent_emails(service, num_emails=5):
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        email_data = []
        for message in messages[:num_emails]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data.append(msg)
        return email_data
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_email_body(msg):
    try:
        parts = msg['payload'].get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                byte_code = base64.urlsafe_b64decode(data.encode('UTF-8'))
                return byte_code.decode("utf-8")
    except Exception as e:
        print(f"Failed to decode email body: {e}")
    return ""

def detect_spam_in_email(email_body):
    result, _ = predict_rf(email_body)
    return result

def real_time_spam_detection():
    service = authenticate_gmail()
    while True:
        emails = get_recent_emails(service)
        for email in emails:
            email_body = get_email_body(email)
            if email_body:
                prediction = detect_spam_in_email(email_body)
                headers = {h["name"]: h["value"] for h in email["payload"]["headers"]}
                from_addr = headers.get("From", "Unknown sender")
                subject = headers.get("Subject", "No Subject")
                print(f"From: {from_addr}")
                print(f"Subject: {subject}")
                print(f"Spam Prediction: {prediction.upper()}")
                print("="*60)
        time.sleep(120)
