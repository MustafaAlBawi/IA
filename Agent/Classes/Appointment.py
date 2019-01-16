from owlready2 import *
import numpy as np

onto = get_ontology('./Agent/Resources/Ontology/AppointmentTypes.owl')
onto.load()

class Appointment:
    def __init__(self, name = "", type_ = "", start_date = None, end_date = None, priority=-1, amount_to_plan = 1, attendees = []):
        self.name = name
        self.type = type_
        self.start_date = start_date
        self.end_date = end_date
        self.amount = int(amount_to_plan)
        self.time_slots = []
        self.priority = priority
        self.attendees = attendees

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

        type_times = onto[self.type.title()].has_time
        return type_times

    def getDayParts(self):
        type_day_parts = []

        if "Night" in onto[self.type.title()].has_part_of_day:
            type_day_parts.extend([0,1,2,3,4,5])
        if "Morning" in onto[self.type.title()].has_part_of_day:
            type_day_parts.extend([6,7,8,9,10,11])
        if "Afternoon" in onto[self.type.title()].has_part_of_day:
            type_day_parts.extend([12,13,14,15,16,17])
        if "Evening" in onto[self.type.title()].has_part_of_day:
            type_day_parts.extend([18,19,20,21,22,23])

        return type_day_parts    
        
    def getAttendees(self):
        return self.attendees

    
    # """ set class functions """
    # def setName(self, name):
    #     self.name = name

    # def setType(self, appointment_type):
    #     self.type = appointment_type
    
    # def setStartDate(self, start_date):
    #     self.start_date = start_date

    # def setEndDate(self, end_date):
    #     self.end_date = end_date
    
    # def addTimeSlot(self, time_slot):
    #     while len(self.time_slots) <= self.amount_to_plan:
    #         self.time_slots.append(time_slot)

    # def setPriority(self, priority):
    #     self.priority = priority

    # def setProperties(self):
    #     return self.properties
        
    # def setAttendees(self, attendees):
    #     return self.attendees

