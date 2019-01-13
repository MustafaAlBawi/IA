#-*- coding: utf-8 -*-

"""

"""
import helpers
# from Classes.Test import Test
from Classes.Appointment import Appointment
from Classes.CalendarAPI import CalendarAPI
"""Start the App"""

def start():
    print("Agent running.")
    ApiHook = CalendarAPI()
    ApiHook.read('2019-01-13T00:00:00.00Z', '2019-01-16T00:00:00.00Z')
    # df = ApiHook.createDateDataFrame('2019-01-13T00:00:00.00Z', '2019-01-14T00:00:00.00Z')
    # ApiHook.insertEvent(df, '2019-01-13')
