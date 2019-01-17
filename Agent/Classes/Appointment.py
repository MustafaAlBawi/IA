from owlready2 import *
import numpy as np

onto = get_ontology('./Agent/Resources/Ontology/AppointmentTypes3.owl')
onto.load()

class Appointment:
    def __init__(self, name = "", type_ = "", start_date = None, end_date = None, priority=-1, amount_to_plan = 1, duration = 1, attendees = []):
        self.name = name
        self.type = type_
        self.start_date = start_date
        self.end_date = end_date
        self.priority = int(priority)
        self.amount = int(amount_to_plan)
        self.duration = int(duration)
        self.attendees = attendees
        self.time_slots = []

    """ get class functions """
    def getName(self):
        return self.name

    def getType(self):
        return self.type
    
    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date

    def getTimeSlots(self):
        return self.time_slots

    def getPriority(self):
        return self.priority
    
    def getTypeTimes(self):
        type_times = onto[self.type.title()].hasTime
        return type_times

    def getClassTimes(self):
        same_class_times = onto[self.type].__class__.instances()
        class_times = []

        for _type in same_class_times:
            class_times.extend(_type.hasTime)

        return class_times

    def getDayParts(self):
        type_day_parts = []

        if "Night" in onto[self.type.title()].hasPartOfDay:
            type_day_parts.extend([0,1,2,3,4,5])
        if "Morning" in onto[self.type.title()].hasPartOfDay:
            type_day_parts.extend([6,7,8,9,10,11])
        if "Afternoon" in onto[self.type.title()].hasPartOfDay:
            type_day_parts.extend([12,13,14,15,16,17])
        if "Evening" in onto[self.type.title()].hasPartOfDay:
            type_day_parts.extend([18,19,20,21,22,23])

        return type_day_parts    
        
    def getAttendees(self):
        return self.attendees
