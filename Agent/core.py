#-*- coding: utf-8 -*-

"""

"""
import helpers
from Classes.CalendarAPI import CalendarAPI
from Classes.Planner import Planner
"""Start the App"""

def start():
    print("Agent running.")
    # load the usercase and create a df to load in the appointments
    appointment = helpers.loadUsercase('Testcase5')
    df = helpers.createDateDataFrame(appointment.start_date, appointment.end_date, 0)

    # Create a hook and set load events into a dataframe
    ApiHook = CalendarAPI()
    for i in range(0, len(appointment.attendees)):
        df = ApiHook.loadCalendarEvents(df, appointment.start_date, appointment.end_date, appointment.attendees[i].id)

    # best_planning = ApiHook.findPosibleEventSpace(df, appointment)
    possible_locations_df = helpers.createDateDataFrame(appointment.start_date, appointment.end_date, 0)
    plan = Planner(df, possible_locations_df, appointment)

    print('plan.best_planning:',plan.best_planning[0])

    # best_planning = ApiHook.findPosibleEventSpace(df, appointment)
    # best_planning = best_planning[0]
    for i in range(0, len(appointment.attendees)):
        for date, time in plan.best_planning[0].items():
            id = appointment.attendees[i].id
            ApiHook.writeToCalendar(time, appointment.type, appointment.priority, appointment.duration, id)
