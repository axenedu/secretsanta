from __future__ import print_function

import base64
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pathlib

WORKING_DIR = pathlib.Path(__file__).parent.resolve()
CREDENTIALS_PATH = WORKING_DIR.joinpath('.env/credentials.json')
TOKEN_PATH = WORKING_DIR.joinpath('.env/token.json')


class GmailAPIAccess:
    # If modifying these scopes, delete the file token.json.
    __SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        # 'https://www.googleapis.com/auth/gmail.readonly',
    ]
    __CREDS = None

    @staticmethod
    def loginGmail():
        """
        Athentication and authorization against gmail
        """
        print(WORKING_DIR)
        if not GmailAPIAccess.__CREDS or not GmailAPIAccess.__CREDS.valid:
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists(TOKEN_PATH):
                GmailAPIAccess.__CREDS = Credentials.from_authorized_user_file(TOKEN_PATH, GmailAPIAccess.__SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not GmailAPIAccess.__CREDS or not GmailAPIAccess.__CREDS.valid:
                if GmailAPIAccess.__CREDS and GmailAPIAccess.__CREDS.expired and GmailAPIAccess.__CREDS.refresh_token:
                    GmailAPIAccess.__CREDS.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_PATH, GmailAPIAccess.__SCOPES)
                    GmailAPIAccess.__CREDS = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'w') as token:
                token.write(GmailAPIAccess.__CREDS.to_json())
        return GmailAPIAccess.__CREDS

    @staticmethod
    def gmail_send_message(to: str, from_recipient: str,subject: str, body: str):
        """Create and send an email message
        Print the returned  message id
        Returns: Message object, including message id

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        creds = GmailAPIAccess.loginGmail()

        try:
            service = build('gmail', 'v1', credentials=creds)
            message = MIMEMultipart('alternative')

            html = MIMEText(body,'html')
            message.attach(html)

            message['To'] = to
            message['From'] = from_recipient
            message['Subject'] = subject



            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }
            # pylint: disable=E1101
            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        return send_message

if __name__ == '__main__':
    template_body = open("../assets/templates/modelo_email.html","r").read()
    template_fixed = template_body.replace("[nombre]", "axenedu").replace("[amigoInvisible]","RCP")
    GmailAPIAccess.gmail_send_message('axenedu@gmail.com','amigoinvisiblesoft@gmail.com','Test2',template_fixed)
