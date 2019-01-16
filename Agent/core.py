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
    appointment = helpers.loadUsercase('Testcase1')

    # Create a hook and set load events into a dataframe
    ApiHook = CalendarAPI()
    #df = ApiHook.loadCalendarEvents('2019-01-14T00:00:00.00Z', '2019-03-17T00:00:00.00Z')
    df = ApiHook.loadCalendarEvents(appointment.start_date, appointment.end_date)
    best_planning = ApiHook.findPosibleEventSpace(df, appointment)
    ApiHook.writeToCalendar(best_planning, appointment.type, appointment.priority)
    #print(possible_df.any())