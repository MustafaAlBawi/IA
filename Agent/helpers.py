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
onto = get_ontology('./Agent/Resources/Ontology/AppointmentTypes.owl')
onto.load()

"""
Load a usercase from the UserCases dir named `name`.
"""
def loadUsercase(name):
    with open('./Agent/Resources/UserCaseses/' + name + '.json') as f:
        data = json.load(f)
        
    #TODO: add amount of appointments to plan
    return Appointment(
        data['name'], 
        data['type'], 
        data['start_date'],
        data['end_date'],
        data['priority'],
        data['amount'],
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
Do stuff with ontology
"""
def getTypeTimes(appointment_type):
    type_times = onto[appointment_type].has_time
    return type_times

def getDayParts(appointment_type):
    type_day_parts = []

    if "Night" in onto[appointment_type].has_part_of_day:
        for i in np.arange(0, 6, 1):
            type_day_parts.extend((i*60))
    if "Morning" in onto[appointment_type].has_part_of_day:
            for i in np.arange(6, 12, 1):
                type_day_parts.extend((i*60))
    if "Afternoon" in onto[appointment_type].has_part_of_day:
        for i in np.arange(12, 18, 1):
            type_day_parts.extend((i*60))
    if "Evening" in onto[appointment_type].has_part_of_day:
        for i in np.arange(18, 23, 1):
            type_day_parts.extend((i*60))

    return type_day_parts    

getTypeTimes("Practice")
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

