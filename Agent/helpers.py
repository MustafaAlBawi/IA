from Classes.UserInput import UserInput
from Classes.Appointment import Appointment
from Classes.Attendee import Attendee
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta, timezone
from dateutil import rrule
from owlready2 import *
import json
from pprint import pprint


"""
Load a usercase from the UserCases dir named `name`.
"""
def loadUsercase(name):
    with open('./Agent/Resources/UserCaseses/' + name + '.json') as f:
        data = json.load(f)

    return Appointment(
        data['name'], 
        data['type'], 
        data['start_date'],
        data['end_date'],
        data['priority'],
        setAttendees(data['attendees']),
        )

"""
Convert the attendees dict to a array of Attendees() objects (Python)
"""
def setAttendees(data_array):
    tmp = []
    for attendee in data_array:
        tmp.append(
            Attendee(attendee['name'], attendee['email'])
            )

    return tmp