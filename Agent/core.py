# -*- coding: utf-8 -*-

"""

"""
import helpers
# from Classes.Test import Test
from Classes.Appointment import Appointment
from Classes.GoogleCalendar import GoogleCalendar

"""Start the App"""

def start():
    print("Agent running.")
    appointment = helpers.createNewAppointment(
        helpers.consoleGetUserInput()
        )