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
    appointments = ApiHook.read('2019-01-13T00:00:00.00Z', '2019-03-10T00:00:00.00Z')
    print(appointments)
    # Appointment = helpers.loadUsercase('euan')
