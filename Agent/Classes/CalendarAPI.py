# from __future__ import print_function
import datetime
from datetime import timedelta
from Classes.Event import Event
from dateutil import parser
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import pprint

class CalendarAPI(object):
    """
    Class that serves the google calendar API
    """
    def __init__(self): # readonly moet weg, want niet alleen lezen maar ook schrijven in calendar
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        self.checkCreds(self.creds)
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))
        self.now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # TODO:
        #add the owner of the current calendar
        self.owner = "EuanTemp2" 
    
    """
    Check the credentials for the google API.
    """
    def checkCreds(self, creds):
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('./Agent/credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    """
    Load all the events from the google calendar API.
    """
    def loadCalendarEvents(self, df, time_min, time_max, calendar_id = 'primary', single_events = True, order_by = 'startTime'):
        events = self.service.events().list(
            timeMin = time_min, 
            timeMax = time_max,
            calendarId = calendar_id,
            singleEvents = single_events,
            orderBy = order_by
            ).execute().get('items', [])
        owner = "EuanTemp"

        if not events:
            print('No upcoming events found.')
            return df

        for event in events:
            start = parser.parse(
                event['start'].get('dateTime', event['start'].get('date'))
                )
            end = parser.parse(
                event['end'].get('dateTime', event['start'].get('date'))
                )

            try:
                event['description']
            except KeyError:
                priority = 1
            else:
                priority = int(event['description'][10])

            duration_in_hours = int(round(divmod((end - start).total_seconds(), 3600)[0]))

            # Check if appointment is longer then 1 full hour.
            if (duration_in_hours < 1):
                print('time of appointment is < 0.')
                continue

            first_hour = int(str(start.time())[0:2])

            for hour in range(0, duration_in_hours):
                # TODO: Checken of dit werkt
                if df[start.date()][first_hour + hour] == 0:
                    event_to_set = Event(owner, priority)
                    df.loc[(first_hour + hour), start.date()] = event_to_set
                else: df[start.date()][first_hour + hour].add_owner(owner, priority)

        return df
        
    def writeToCalendar(self, best_planning, type, priority, duration, id):
        best_planning = parser.parse(best_planning)
        best_planning -= timedelta(hours=1)

        end_best_planning = best_planning + timedelta(hours=duration)
        startEv = str(best_planning.date()) + 'T' + str(best_planning.time()) + 'Z'
        endEv = str(end_best_planning.date()) + 'T' + str(end_best_planning.time()) + 'Z'

        # Insert event to google calendar
        event = {
            'summary': type,
            'location': '',
            'description': 'priority:#' + str(priority),
            'start': {
                'dateTime': startEv,
                'timeZone': 'Europe/Amsterdam',
            },
            'end': {
                'dateTime': endEv,
                'timeZone': 'Europe/Amsterdam',
            },
            'recurrence': [
            ],
            'attendees': [
            ],
            'reminders': {
                'useDefault': True,

            },
        }

        event = self.service.events().insert(calendarId=id, body=event).execute()