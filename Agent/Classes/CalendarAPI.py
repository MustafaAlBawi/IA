# from __future__ import print_function
import datetime
from dateutil import parser
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

class CalendarAPI(object):
    """
    Class that serves the google calendar API
    """
<<<<<<< Updated upstream
    def __init__(self, scope='readonly'):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.' + scope
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        self.checkCreds(self.creds)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))
        self.now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    def checkCreds(self, creds):
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('./Agent/credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    def read(self, time_min, time_max, calendar_id = 'primary', single_events = True, order_by = 'startTime'):
        events_results = self.service.events().list(
            timeMin = time_min, 
            timeMax = time_max,
            calendarId = calendar_id, 
            maxResults = 10,
            singleEvents = single_events,
            orderBy = order_by
            ).execute()

        events = events_results.get('items', [])
        print(events)
        exit()
        df = self.createDateDataFrame(time_min, time_max)

        # TODO:
        # Hier onder moeten de evenementen een voor een worden ingeladen.
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            print(events[0])
            startDate = start[8:10]
            startTime = start[11:13]
            endDate = end[8:10]
            endTime = end[11:13]

            print(startDate, startTime, endDate, endTime)

            startTime = int(startTime)
            endTime = int(endTime)
            loop = endTime - startTime + 1
            for i in range(0,loop):
                df.set_value(startTime + i, int(startDate), 1)

        return df

    def createDateDataFrame(self, start_date, end_date):
        columns = pd.date_range(start=start_date, end=end_date, freq='D')
        index = range(1, 25)
        return pd.DataFrame(None, index=index, columns=columns)

    def insertEvent(self, df, date, time, priority = 2):
        eventStart = int(10)
        eventEnd = int(12)
        eventfound = 0
        Date = 0
        Time = 0

        start_date = '2019-03-04'
        start_date_object = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
        end_date = '2019-03-10'
        for j in range(int(start_date[8:10]), int(end_date[8:10])):
            for i in range(eventStart, int(eventEnd) + 1):
                timeslot = df.get_value(i, start_date_object)

                if timeslot == 0:
                    df.set_value(int(i), start_date_object, 2)
                    print(timeslot)
                    Date = start_date_object
                    Time = i
                    print('Date:', Date, 'Time:', i)
                    print('Planned the event')
                    eventfound = 1
                    break
            if eventfound == 1:
                break
            start_date_object += datetime.timedelta(days=1)
        if eventfound == 0:
            print('Could not find timeslot')
        print(df)

        # TODO:
        # de colom kan worden opgehaald als string of met een datetime.
        # de rij zijn dan de uuren. De uren waarop een afspraak duurt 
        # moeten dus worden ingevuld met een priority score.
        column = df[date][time] = priority
        print(column)

    def writeInCalendar():
        endTime = int(Time)
        Time = int(Time) - 1
        startEv = datetime.datetime.combine(start_date_object, datetime.time(Time, 0, 0))
        endEv = datetime.datetime.combine(start_date_object, datetime.time(endTime, 0, 0))
        startEv = str(startEv.date()) + 'T' + str(startEv.time()) + 'Z'
        endEv = str(endEv.date()) + 'T' + str(endEv.time()) + 'Z'
        print(startEv, endEv)

        # Insert event to google calendar
        event = {
            'summary': 'KoffieTest',
            'location': 'unknown',
            'description': 'Getting coffee',
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

        event = service.events().insert(calendarId='primary', body=event).execute()

# TODO:
# Code hier onder moet deels nog omgezet worden in d CalendarAPI class.
# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     store = file.Storage('token.json')
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#         creds = tools.run_flow(flow, store)
#     service = build('calendar', 'v3', http=creds.authorize(Http()))

#     # Call the Calendar API
#     now = '2019-03-04T00:00:00.00Z' #datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     end = '2019-03-10T00:00:00.00Z'

#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now, timeMax =end ,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     column = pd.Series(range(4, 10))
#     row = pd.Series(range(0, 25))
#     df = pd.DataFrame(0, index=row, columns=column)

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         end = event['end'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])
#         print(events[0])
#         startDate = start[8:10]
#         startTime = start[11:13]
#         endDate = end[8:10]
#         endTime = end[11:13]

#         print(startDate, startTime, endDate, endTime)

#         startTime = int(startTime)
#         endTime = int(endTime)
#         loop = endTime - startTime + 1
#         for i in range(0,loop):
#             df.set_value(startTime + i, int(startDate), 1)

#     print(df)

#     #Plan event
#     eventName = 'koffie'
#     eventStart = int(10)
#     eventDuration = int(1)
#     eventEnd = int(12)
#     eventfound = 0
#     Date = 0
#     Time = 0
#     for j in range(4, 10):
#         for i in range(eventStart,int(eventEnd)+1):
#             timeslot = df.get_value(i,j)

#             if timeslot == 0:
#                 df.set_value(int(i), int(j), 2)
#                 print(timeslot)
#                 Date = j
#                 Time = i
#                 print('Date:', j, 'Time:', i)
#                 print('Planned the event')
#                 eventfound = 1
#                 break
#         if eventfound == 1:
#             break

#     if eventfound == 0:
#         print('Could not find timeslot')
#     print(df)
#     endTime = int(Time) - 1
#     Time = int(Time) - 2
#     startEv = '2019-03-0'+str(Date)+'T'+str(Time)+':00:00.00Z'
#     endEv = '2019-03-0'+str(Date)+'T'+str(endTime)+':00:00.00Z'
#     print(startEv)
#     print(endEv)
#     #Insert event to google calendar
#     event = {
#         'summary': 'KoffieTest',
#         'location': 'unknown',
#         'description': 'Getting coffee',
#         'start': {
#             'dateTime': startEv,
#             'timeZone': 'Europe/Amsterdam',
#         },
#         'end': {
#             'dateTime': endEv,
#             'timeZone': 'Europe/Amsterdam',
#         },
#         'recurrence': [
#         ],
#         'attendees': [
#         ],
#         'reminders': {
#             'useDefault': True,

#         },
#     }

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print
#     'Event created: %s' % (event.get('htmlLink'))
# if __name__ == '__main__':
#     main()
=======
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = '2019-03-04T00:00:00.00Z' #datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end = '2019-03-10T00:00:00.00Z'

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax =end ,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    column = pd.Series(range(4, 10))
    row = pd.Series(range(0, 25))
    df = pd.DataFrame(0, index=row, columns=column)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        print(events[0])
        startDate = start[8:10]
        startTime = start[11:13]
        endDate = end[8:10]
        endTime = end[11:13]

        print(startDate, startTime, endDate, endTime)

        startTime = int(startTime)
        endTime = int(endTime)
        loop = endTime - startTime + 1
        for i in range(0,loop):
            df.set_value(startTime + i, int(startDate), 1)

    print(df)

    #Plan event
    eventName = 'koffie'
    eventStart = int(10)
    eventDuration = int(1)
    eventEnd = int(12)
    eventfound = 0
    Date = 0
    Time = 0
    for j in range(4, 10):
        for i in range(eventStart,int(eventEnd)+1):
            timeslot = df.get_value(i,j)

            if timeslot == 0:
                df.set_value(int(i), int(j), 2)
                print(timeslot)
                Date = j
                Time = i
                print('Date:', j, 'Time:', i)
                print('Planned the event')
                eventfound = 1
                break
        if eventfound == 1:
            break

    if eventfound == 0:
        print('Could not find timeslot')
    print(df)


    ##WRITE TO GOOGLE CALENDAR
    endTime = int(Time) - 1
    Time = int(Time) - 2
    startEv = '2019-03-0'+str(Date)+'T'+str(Time)+':00:00.00Z'
    endEv = '2019-03-0'+str(Date)+'T'+str(endTime)+':00:00.00Z'
    print(startEv)
    print(endEv)
    event = {
        'summary': 'KoffieTest',
        'location': 'unknown',
        'description': 'Getting coffee',
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

    event = service.events().insert(calendarId='primary', body=event).execute()
    print
    'Event created: %s' % (event.get('htmlLink'))
if __name__ == '__main__':
    main()
>>>>>>> Stashed changes
