# from __future__ import print_function
import datetime
from datetime import timedelta
from Classes.Event import Event
from dateutil import parser
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd

class CalendarAPI(object):
    """
    Class that serves the google calendar API
    """
    def __init__(self, scope='readonly'): # readonly moet weg, want niet alleen lezen maar ook schrijven in calendar
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.' + scope
        self.store = file.Storage('token.json')
        self.creds = self.store.get()
        self.checkCreds(self.creds)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))
        self.now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # TODO:
        #add the owner of the current calendar
        self.owner = "EuanTemp2" 
    
    def checkCreds(self, creds):
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('./Agent/credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    def createDateDataFrame(self, start_date, end_date, filler):
        columns = pd.date_range(start=start_date, end=end_date, freq='D')
        index = range(1, 25) # uren in een dag
        return pd.DataFrame(filler, index=index, columns=columns)

    def loadCalendarEvents(self, time_min, time_max, calendar_id = 'primary', single_events = True, order_by = 'startTime'):
        events = self.service.events().list(
            timeMin = time_min, 
            timeMax = time_max,
            calendarId = calendar_id, 
            maxResults = 10,
            singleEvents = single_events,
            orderBy = order_by
            ).execute().get('items', [])
        owner = "EuanTemp"

        df = self.createDateDataFrame(time_min, time_max, 0)

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
            if event['summary'].startswith("priority:#"):
                priority = event['summary'][10]
            else: priority = 1

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

    def makeTotalDF(self, df, appointment):
        possible_timeslots = self.createDateDataFrame(appointment.start_date, appointment.end_date, 0)

        for day in df:
            for slot in range(1, len(df[day]) + 1):
                if df[day][slot] == 0:
                    possible_timeslots[day][slot] = 0
                elif (df[day][slot] != 0 and (df[day][slot].getHighest() < int(appointment.priority))):
                    possible_timeslots[day][slot] = df[day][slot].getHighest()
        
        return possible_timeslots

    def findPosibleEventSpace(self, df, appointment):
        possible_timeslots = self.makeTotalDF(df, appointment)

        type_times = appointment.getTypeTimes()
        day_parts = appointment.getDayParts()

        conflict_dict = { # moet gevuld worden om beste keuze te kunnen gaan maken
        # gevuld adhv ontology
            "no_conflict": self.noConflictFillDict(possible_timeslots, type_times), 
            "nc_part_day": self.noConflictFillDict(possible_timeslots, day_parts),
            "priority_conflict": self.conflictFillDict(possible_timeslots, type_times, appointment.getPriority()),
            "pc_part_day": self.conflictFillDict(possible_timeslots, day_parts, appointment.getPriority())
        }
        #TODO:
        ## probeer per dict alles in te plannen
        print(conflict_dict["no_conflict"])
        return possible_timeslots # temp


    def noConflictFillDict(self, possible_timeslots, times_array):
        res_dict = dict()
        for day in possible_timeslots:
            for slot in range(1, len(possible_timeslots[day]) + 1):
                type_times = []
                
                for j in range(len(times_array)):
                    i = j -1
                    type_times.append(day + timedelta(hours=times_array[i]))
                    if ((possible_timeslots[day][slot] == 0) and (day + timedelta(hours=slot)) == type_times[i]):
                        res_dict[day + timedelta(hours=slot)] = 0
        return res_dict
    
    def conflictFillDict(self, possible_timeslots, times_array, priority):
        res_dict = dict()
        for day in possible_timeslots:
            for slot in range(1, len(possible_timeslots[day]) + 1):
                type_times = []
                
                for j in range(len(times_array)):
                    i = j -1
                    type_times.append(day + timedelta(hours=times_array[i]))
                    if ((possible_timeslots[day][slot] != 0) and (possible_timeslots[day][slot] < int(priority))):
                        if (day + timedelta(hours=slot)) == type_times[i]:
                            res_dict[day + timedelta(hours=slot)] = possible_timeslots[day][slot]
        return res_dict
        
