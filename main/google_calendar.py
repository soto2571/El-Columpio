import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import pickle
from google.auth.transport.requests import Request

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')


def authenticate_google():
    creds = None

    # Check if credentials already exist in token.pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Validate credentials or reauthenticate if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Trigger the authentication flow
            flow = InstalledAppFlow.from_client_config(
                {
                    "web": {
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "redirect_uris": [REDIRECT_URI],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                SCOPES,
            )
            creds = flow.run_local_server(port=8000)

            # Save the credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    return creds


def create_google_calendar_event(reservation):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    # Combine date and time for event start
    start_time = datetime.datetime.combine(reservation.date, reservation.time)
    end_time = start_time + datetime.timedelta(hours=1)  # Default event duration is 1 hour

    event = {
        'summary': f"Reservation for {reservation.customer_name}",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Puerto_Rico',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Puerto_Rico',
        },
        'attendees': [
            {'email': reservation.email},
        ],
    }

    try:
        # Insert event into Google Calendar
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return event
    except Exception as error:
        print(f"An error occurred: {error}")
        raise