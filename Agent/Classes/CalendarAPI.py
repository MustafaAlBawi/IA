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

    def retrieveCalendarID(self):
        page_token = None
        calendar_id_list = []
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendar_id_list.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        return calendar_id_list

    def read(self, time_min, time_max, calendar_id = 'primary', single_events = True, order_by = 'startTime'):
        events_results = self.service.events().list(
            timeMin = time_min, 
            timeMax = time_max,
            calendarId = calendar_id,
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

            if startTime: #Failsafe for multiple day events which have no time.
                startTime = int(startTime)
                endTime = int(endTime)
                loop = endTime - startTime
                for i in range(0,loop):
                    df.set_value(startTime + i, int(startDate), 1)

        return df

    def createDateDataFrame(self, start_date, end_date):
        columns = pd.date_range(start=start_date, end=end_date, freq='D')
        index = range(1, 25)
        return pd.DataFrame(0, index=index, columns=columns)

    def insertEvent(self, df, eventStart, eventEnd, start_date, end_date, priority = 2, eventfound = 0, Time = 0):
        eventStart = int(10)
        eventEnd = int(12)
        eventDuration = int(2)
        eventfound = 0
        Date = 0
        Time = 0
        counter = 1
        start_date = '2019-03-04'
        start_date_object = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
        end_date = '2019-03-10'
        for j in range(int(start_date[8:10]), int(end_date[8:10])):
            for i in range(eventStart, int(eventEnd) + 1):
                timeslot = df.get_value(i, start_date_object)

                if timeslot == 0:
                    df.set_value(int(i), start_date_object, 2)
                    if eventDuration > 1:
                        for k in range(1, eventDuration):
                            timeslot = df.get_value(int(i + k), start_date_object)
                            if timeslot == 0:
                                df.set_value(int(i + k), start_date_object, 2)
                                counter += 1
                            else:
                                counter = 1
                                break
                    if counter == eventDuration:
                        Date = start_date_object
                        Time = i - 1
                        print('Date:', Date, 'Time:', i - 1)
                        print('Planned the event')
                        eventfound = 1
                        break
            if eventfound == 1:
                break
            start_date_object += datetime.timedelta(days=1)
        if eventfound == 0:
            print('Could not find timeslot')

        # TODO:
        # de colom kan worden opgehaald als string of met een datetime.
        # de rij zijn dan de uuren. De uren waarop een afspraak duurt 
        # moeten dus worden ingevuld met een priority score.
        column = df[date][time] = priority
        print(column)

        return start_date_object, Time

    def writeInCalendar(start_date_object, Time, event_name, event_description):
        event_name = 'Koffietest'
        event_description = 'Getting coffee'
        endTime = int(Time) + eventDuration - 1
        Time = int(Time) - 1

        startEv = datetime.datetime.combine(start_date_object, datetime.time(Time, 0, 0))
        endEv = datetime.datetime.combine(start_date_object, datetime.time(endTime, 0, 0))
        startEv = str(startEv.date()) + 'T' + str(startEv.time()) + 'Z'
        endEv = str(endEv.date()) + 'T' + str(endEv.time()) + 'Z'

        print(startEv, endEv)

        # Insert event to google calendar
        event = {
            'summary': event_name,
            'location': 'unknown',
            'description': event_description,
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
        print("Planned the event in the google calendar")

    def loadCalendarEvents(self, time_min, time_max, calendar_id = 'primary', single_events = True, order_by = 'startTime'):
        events = self.service.events().list(
            timeMin = time_min, 
            timeMax = time_max,
            calendarId = calendar_id, 
            maxResults = 10,
            singleEvents = single_events,
            orderBy = order_by
            ).execute().get('items', [])

        df = self.createDateDataFrame(time_min, time_max)

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

            duration_in_hours = int(round(divmod((end - start).total_seconds(), 3600)[0]))

            # Check if appointment is longer then 1 full hour.
            if (duration_in_hours < 1):
                print('time of appointment is < 0.')
                continue

            first_hour = int(str(start.time())[0:2])

            for hour in range(0, duration_in_hours):
                # TODO: Event invullen ipv 1
                df[start.date()][first_hour + hour] = 1

        return df

    def findPosibleEventSpace(self, df, appointment):
        posible_timeslots = self.createDateDataFrame(appointment.start_date, appointment.end_date)

        for day in posible_timeslots:
            for slot in range(1, len(df[day]) + 1):
                if (df[day][slot] < int(appointment.priority)): # Hier meer logica om te kijken of het slot echt geschikt is?
                    posible_timeslots.loc[slot, day] = True
  
        return posible_timeslots
