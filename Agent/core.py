#-*- coding: utf-8 -*-

"""

"""
import helpers
# from Classes.Test import Test
from Classes.Appointment import Appointment
from Classes.CalendarAPI import CalendarAPI
from Classes.Event import Event
"""Start the App"""

def start():
    print("Agent running.")
    # load the usercase
    appointment = helpers.loadUsercase('Testcase5')
    # Create a hook and set load events into a dataframe
    ApiHook = CalendarAPI()

    df = ApiHook.createDateDataFrame(appointment.start_date, appointment.end_date, 0)

    for i in range(0, len(appointment.attendees)):
        print(appointment.attendees[i].id)
        df = ApiHook.loadCalendarEvents(df, appointment.start_date, appointment.end_date, appointment.attendees[i].id)
    print(df)

    best_planning = ApiHook.findPosibleEventSpace(df, appointment)
    best_planning = best_planning[0]
    for i in range(0, len(appointment.attendees)):
        for date, time in best_planning.items():
            id = appointment.attendees[i].id
            ApiHook.writeToCalendar(time, appointment.type, appointment.priority, appointment.duration, id)
