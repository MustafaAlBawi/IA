from Classes.UserInput import UserInput
from Classes.Appointment import Appointment
from Classes.Attendee import Attendee
from Classes.CalendarAPI import CalendarAPI
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta, timezone
from dateutil import rrule
from owlready2 import *
import numpy as np
import json
from pprint import pprint

#onto = get_ontology("file://C:/Users/Gebruiker/Documents/Euan/Studie/ArtificialIntelligence/Blok2-2018/IntelligentAgents/Project/IntelAgents-Git/tgGit/Agent/Resources/AppointmentTypes.owl")
#onto.load()
onto = get_ontology('file://C:/Users/tycho/Desktop/tgGit/Agent/Resources/Ontology/AppointmentTypes.owl')
onto.load()

"""
Load a usercase from the UserCases dir named `name`.
"""
def loadUsercase(name):
    with open('C:/Users/tycho/Desktop/tgGit/Agent/Resources/UserCaseses/' + name + '.json') as f:
        data = json.load(f)
        
    #TODO: add amount of appointments to plan
    return Appointment(
        data['name'], 
        data['type'], 
        data['start_date'],
        data['end_date'],
        data['priority'],
        data['amount'],
        data['duration'],
        setAttendees(data['attendees']),
        )

"""
Convert the attendees dict to a array of Attendees() objects (Python)
"""
def setAttendees(data_array):
    tmp = []
    for attendee in data_array:
        tmp.append(
            Attendee(attendee['name'], attendee['email'], attendee['id'])
            )

    return tmp

"""
Look for best Date and Time to set appointment
"""
def searchPotentialTimes(appointment):
    attendees_calendars = []

    for attendee in appointment.getAttendees():
        attendees_calendars.append(
            CalendarAPI.reader(appointment.start_date, appointment.end_date)
            )
    
    
    #TODO:
    #appointment_type = str(appointment.getType())
    #type_times = onto[appointment_type].Time

