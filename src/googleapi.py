from __future__ import print_function
import json, os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CLIENT_TOKEN  = '../data/token.json'
CLIENT_SECRET = '../data/client_secret.json'

def authenticate(token, secret, sheet_id):

    """Shows basic usage of the Sheets API.
    Returns sheet function
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token, 'w') as token:
            token.write(creds.to_json())

    # Call the Sheets API and return a sheet
    service = build('sheets', 'v4', credentials=creds)

    def sheet(**kwargs):
      return service.spreadsheets().values().batchGet(
        spreadsheetId=sheet_id, **kwargs).execute().get("valueRanges",[])

    return sheet

if __name__ == '__main__':

    sheet_id = '1vViMWDsMRnbGUgP44XNDlQrLQ3MsdgO9W91mM4MxJtw'
    names = [
      'education',
      'work',
      'papers',
      'teaching',
      'awards',
      'presentations',
      'colabs',
      'perform',
      'adminis',
    ]

    sheet = authenticate(CLIENT_TOKEN, CLIENT_SECRET, sheet_id)

    original = sheet(ranges=[ f"{name}Final!A:Z" for name in names ])
    with open("../data/sheets_english.json", "w") as eng:
        json.dump(original, eng, indent=4, ensure_ascii=False)

    translated = sheet(ranges=[ f"{name}Translated!A:Z" for name in names ])
    with open("../data/sheets_german.json", "w") as ger:
        json.dump(translated, ger, indent=4, ensure_ascii=False)
