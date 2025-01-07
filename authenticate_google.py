from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the required Google Calendar scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no credentials or the credentials are invalid/expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        
        # Save the new credentials to token.pickle
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    print("Authentication successful.")

if __name__ == '__main__':
    main()