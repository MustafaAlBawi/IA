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
    
    def checkCreds(self, creds):
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('C:/Users/tycho/Desktop/tgGit/Agentcredentials.json', self.SCOPES)
            creds = tools.run_flow(flow, self.store)

    def createDateDataFrame(self, start_date, end_date, filler):
        endDay = int(end_date[8:10]) - 1
        end_date = end_date[:8] + str(endDay) + end_date[10:]
        columns = pd.date_range(start=start_date, end=end_date, freq='D')
        index = range(1, 25) # uren in een dag
        return pd.DataFrame(filler, index=index, columns=columns)

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
            print(event)
            try:
                event['description']
            except KeyError:
                priority = 1
            else:
                print(event['description'])
                priority = int(event['description'][9])

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

        conflict_dicts = { # moet gevuld worden om beste keuze te kunnen gaan maken
        # gevuld adhv ontology
            "no_conflict": self.noConflictFillDict(possible_timeslots, type_times), 
            "nc_part_day": self.noConflictFillDict(possible_timeslots, day_parts),
            "priority_1_conflict": self.conflictFillDict(possible_timeslots, type_times, appointment.getPriority(), 1),
            "pc_1_part_day": self.conflictFillDict(possible_timeslots, day_parts, appointment.getPriority(), 1),
            "priority_2_conflict": self.conflictFillDict(possible_timeslots, type_times, appointment.getPriority(), 2),
            "pc_2_part_day": self.conflictFillDict(possible_timeslots, day_parts, appointment.getPriority(), 2),
            "priority_3_conflict": self.conflictFillDict(possible_timeslots, type_times, appointment.getPriority(), 3),
            "pc_3_part_day": self.conflictFillDict(possible_timeslots, day_parts, appointment.getPriority(), 3),
            "priority_4_conflict": self.conflictFillDict(possible_timeslots, type_times, appointment.getPriority(), 4),
            "pc_4_part_day": self.conflictFillDict(possible_timeslots, day_parts, appointment.getPriority(), 4)
        }
        order_dict = ["no_conflict", "nc_part_day", "priority_1_conflict", "pc_1_part_day", \
            "priority_2_conflict", "pc_2_part_day", "priority_3_conflict", "pc_3_part_day", \
            "priority_4_conflict", "pc_4_part_day"]

        returned_times_priorsum = self.findBestPlanning(possible_timeslots, conflict_dicts, order_dict, appointment)

        return returned_times_priorsum # temp

    def findBestPlanning(self, possible_timeslots, conflict_dicts, order_dict, appointment):
        times_taken = dict()
        priority_sum = 0
        first_day = datetime.datetime(int(appointment.start_date[0:4]), int(appointment.start_date[5:7]),
                                      int(appointment.start_date[8:10]))
        last_day = datetime.datetime(int(appointment.end_date[0:4]), int(appointment.end_date[5:7]),
                                     int(appointment.end_date[8:10]))

        for book in order_dict:
            cur_book = conflict_dicts[book]
            day = first_day
            while day != last_day + timedelta(days=1):
                for hour in range(0, 24):
                    cur_time_stamp = (day + timedelta(hours=hour))
                    cur_time = (str(cur_time_stamp.date()) + " " + str(cur_time_stamp.time()))
                    if len(times_taken) == appointment.amount:
                        break
                    elif not (day in times_taken) and (cur_time in cur_book.keys()):
                        print(appointment.duration)
                        extra_hours = (appointment.duration - 1)
                        for extra in range(extra_hours):
                            next_hour_stamp = cur_time_stamp + timedelta(hours=extra)
                            next_hour = (str(next_hour_stamp.date()) + " " + str(next_hour_stamp.time()))
                            if (next_hour in cur_book.keys()):
                                pass
                            else:
                                break
                        times_taken[day] = cur_time
                        print(len(times_taken))
                        priority_sum += cur_book[cur_time]
                day += timedelta(days=1)

        print('best time:',times_taken, priority_sum)
        return times_taken, priority_sum

    def noConflictFillDict(self, possible_timeslots, times_array):
        res_dict = dict()
        for day in possible_timeslots:
            for slot in range(1, len(possible_timeslots[day]) + 1):
                type_times = []
                
                for j in range(len(times_array)):
                    i = j -1
                    type_times.append(day + timedelta(hours=times_array[i]))
                    if ((possible_timeslots[day][slot] == 0) and (day + timedelta(hours=slot)) == type_times[i]):
                        time_stamp = day + timedelta(hours=slot)
                        date_time, hour_time = time_stamp.date(), time_stamp.time()
                        res_dict[str(date_time) + " " + str(hour_time)] = 0
        return res_dict
    
    def conflictFillDict(self, possible_timeslots, times_array, app_priority, cur_max_priority):
        res_dict = dict()
        return res_dict #temp

        for day in possible_timeslots:
            for slot in range(1, len(possible_timeslots[day]) + 1):
                type_times = []
                
                for j in range(len(times_array)):
                    i = j -1
                    type_times.append(day + timedelta(hours=times_array[i]))
                    if ((possible_timeslots[day][slot] != 0) and (possible_timeslots[day][slot] < int(app_priority)) and \
                    (possible_timeslots[day][slot] <= cur_max_priority)):
                        if (day + timedelta(hours=slot)) == type_times[i]:
                            res_dict[day + timedelta(hours=slot)] = possible_timeslots[day][slot]
        return res_dict
        
    def writeToCalendar(self, best_planning, type, priority, duration):
        best_planning = str(best_planning[0])
        date = best_planning
        time = int(best_planning[51:53]) - 1
        if(int(time) + duration < 23):
            endTime = int(time) + duration
            endDay = int(date[48:50])
        else:
            endTime = int(time) + duration - 24
            endDay = int(date[48:50]) + 1

        startEv = datetime.datetime.combine(datetime.date(int(date[40:44]),int(date[45:47]),int(date[48:50])), datetime.time(time, 0, 0))
        endEv = datetime.datetime.combine(datetime.date(int(date[40:44]),int(date[45:47]),endDay), datetime.time(endTime, 0, 0))

        startEv = str(startEv.date()) + 'T' + str(startEv.time()) + 'Z'
        endEv = str(endEv.date()) + 'T' + str(endEv.time()) + 'Z'
        print(startEv, endEv)

        # Insert event to google calendar
        event = {
            'summary': type,
            'location': '',
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

        event = self.service.events().insert(calendarId='primary', body=event).execute()