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
import pandas as pd

onto = get_ontology('./Agent/Resources/Ontology/NewApps.owl')
onto.load()

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
Create a DataFrame
"""
def createDateDataFrame(start_date, end_date, filler):
    endDay = int(end_date[8:10]) - 1
    end_date = end_date[:8] + str(endDay) + end_date[10:]
    columns = pd.date_range(start=start_date, end=end_date, freq='D')
    index = range(1, 25) # uren in een dag
    return pd.DataFrame(filler, index=index, columns=columns)

