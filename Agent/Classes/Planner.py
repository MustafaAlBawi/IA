import pandas as pd
import datetime
from datetime import timedelta
from collections import OrderedDict

class Planner(object):
    def __init__(self, all_appointments_df, possible_timeslots_df,appointment):
        self.all_appointments_df = all_appointments_df
        self.appointment = appointment
        self.highest_df = self.getHighestPriority(all_appointments_df, possible_timeslots_df, appointment)

        # Empty dict with appointments according to priority
        
        self.conflict_dicts = OrderedDict([
            ("no_conflict", self.noConflictFillDict(self.highest_df, appointment.getTypeTimes(), appointment.priority)), 
            ("nc_part_day", self.noConflictFillDict(self.highest_df, appointment.getClassTimes(), appointment.priority)),
            ("priority_1_conflict", self.conflictFillDict(self.highest_df, appointment.getTypeTimes(), appointment.priority, 1)),
            ("pc_1_part_day", self.conflictFillDict(self.highest_df, appointment.getClassTimes(), appointment.priority, 1)),
            ("priority_2_conflict", self.conflictFillDict(self.highest_df, appointment.getTypeTimes(), appointment.priority, 2)),
            ("pc_2_part_day", self.conflictFillDict(self.highest_df, appointment.getClassTimes(), appointment.priority, 2)),
            ("priority_3_conflict", self.conflictFillDict(self.highest_df, appointment.getTypeTimes(), appointment.priority, 3)),
            ("pc_3_part_day", self.conflictFillDict(self.highest_df, appointment.getClassTimes(), appointment.priority, 3)),
            ("priority_4_conflict", self.conflictFillDict(self.highest_df, appointment.getTypeTimes(), appointment.priority, 4)),
            ("pc_4_part_day", self.conflictFillDict(self.highest_df, appointment.getClassTimes(), appointment.priority, 4))
        ])
        # Set the order of priority dict.
        self.order_list = [
            "no_conflict", 
            "nc_part_day", 
            "priority_1_conflict", 
            "pc_1_part_day",
            "priority_2_conflict", 
            "pc_2_part_day", 
            "priority_3_conflict", 
            "pc_3_part_day", 
            "priority_4_conflict", 
            "pc_4_part_day"
            ]
            
        self.best_plan = self.findBestPlanning(self.highest_df, self.conflict_dicts, self.order_list, self.appointment)

    def getHighestPriority(self, all_appointments_df, possible_timeslots_df, appointment):
        for day in all_appointments_df:
            for slot in range(1, len(all_appointments_df[day]) + 1):
                if all_appointments_df[day][slot] == 0:
                    possible_timeslots_df[day][slot] = 0
                else:
                    possible_timeslots_df[day][slot] = all_appointments_df[day][slot].getHighest()
        return possible_timeslots_df

    def findBestPlanning(self, possible_timeslots, conflict_dicts, order_dict, appointment):
        times_taken = dict()
        priority_sum = 0
        first_day = datetime.datetime(int(appointment.start_date[0:4]), int(appointment.start_date[5:7]),
                                      int(appointment.start_date[8:10]))
        last_day = datetime.datetime(int(appointment.end_date[0:4]), int(appointment.end_date[5:7]),
                                     int(appointment.end_date[8:10]))
        for counter in range(0,len(conflict_dicts)):
            if (counter / 2) < appointment.priority:
                cur_book = conflict_dicts[self.order_list[counter]]
                day = first_day
                while day != last_day + timedelta(days=1):
                    for hour in range(0, 24):
                        cur_time_stamp = (day + timedelta(hours=hour))
                        cur_time = (str(cur_time_stamp.date()) + " " + str(cur_time_stamp.time()))
                        if len(times_taken) == appointment.amount:
                            break
                        elif not (day in times_taken) and (cur_time in cur_book.keys()):
                            extra_hours = (appointment.duration - 1)
                            for extra in range(extra_hours):
                                next_hour_stamp = cur_time_stamp + timedelta(hours=extra)
                                next_hour = (str(next_hour_stamp.date()) + " " + str(next_hour_stamp.time()))
                                if (next_hour not in cur_book.keys() and self.highest_df[day][hour + extra] < appointment.priority):
                                    break

                            times_taken[day] = cur_time
                            priority_sum += cur_book[cur_time]
                    day += timedelta(days=1)
            else: 
                continue

        return times_taken, priority_sum


    def noConflictFillDict(self, possible_timeslots, times_array, priority):
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