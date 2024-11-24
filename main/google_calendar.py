import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pickle
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    # Load credentials from token.pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Check if the loaded object is valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentaials found. Please reauthenticate using the authentication script.")
    
    return creds

def create_google_calendar_event(reservation):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.datetime.combine(reservation.date, reservation.time)
    end_time = start_time + datetime.timedelta(hours=1)

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
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as error:
        print(f"An error occurred: {error}")
        raise 