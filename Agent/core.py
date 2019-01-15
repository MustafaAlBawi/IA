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
    appointment = helpers.loadUsercase('euan')

    # Create a hook and set load events into a dataframe
    ApiHook = CalendarAPI()
    df = ApiHook.loadCalendarEvents('2019-01-14T00:00:00.00Z', '2019-03-17T00:00:00.00Z')
    posible_df = ApiHook.findPosibleEventSpace(df, appointment)
    print(posible_df.all())