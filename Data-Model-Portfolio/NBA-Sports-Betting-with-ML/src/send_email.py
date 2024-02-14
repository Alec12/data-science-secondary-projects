import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import datetime
from time import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from src.predict_spread import predict_new_data

# client_secret = df = pd.read_json("data/client_secret.json")

def send_predictions(email, pdate):
    t0 = time()
    # Define your email parameters
    sender_email = email
    receiver_email = email
    subject = 'NBA Model Predictions for : ' + pdate
    message_text = 'Please find the attached Sports Bets.'

    # Convert DataFrame to CSV
    new_predictions = predict_new_data()
    csv_content = new_predictions.to_csv(index=False)

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = email
    message['Subject'] = subject

    # Attach the message text
    message.attach(MIMEText(message_text, 'plain'))

    # Attach the CSV file
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(csv_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='predictions.csv')
    message.attach(attachment)

    # Load Gmail API credentials
    creds = None
    token_file = 'token.json'
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("data/client_secret.json", ['https://www.googleapis.com/auth/gmail.send'])
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Send the email
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    print("Data Sent Over Email Complete. Execution time : %.2fs" % (time() - t0))
