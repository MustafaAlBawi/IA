from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleCalendar(object):
    """
    Class that serves the google calendar API
    """
    def __init__(self, scope='readonly'):
        """[summary]
        
        Arguments:
            object {[type]} -- [description]
        
        Keyword Arguments:
            scope {str} -- [description] (default: {'readonly'})
        """

        self.SCOPES = 'https://www.googleapis.com/auth/calendar.' + scope
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        self.checkCreds(self.creds)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))
        self.now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    def checkCreds(self, creds):
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    def events(self, calendar_id, time_min, max_results, single_events, order_by):
        return self.service.events().list(calendarId=calendar_id, 
                                        timeMin=time_min,
                                        maxResults=max_results, 
                                        singleEvents=single_events,
                                        orderBy=order_by).execute()

    def test(self):
        # Call the Calendar API 
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=self.now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])