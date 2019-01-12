from owlready import *

onto = get_ontology("./Resources/AppointmentTypes.owl")
onto.load()

class Appointment:
    def __init__(self):
        #class properties (with __init__ value)
        self.name = ""
        self.type = ""
        self.start_date = None
        self.end_date = None
        self.priority = -1
        self.super_types = []
        self.properties = []
        self.attendees = []

    """ set class functions """
    def setName(self, name):
        self.name = name

    def setType(self, appointment_type):
        try:
            self.type = onto[appointment_type]
        except:
            print("There is no such type appointment in the ontology")
    
    def setStartDate(self, start_date):
        self.start_date = start_date

    def setEndDate(self, end_date):
        self.end_date = end_date

    def setPriority(self, priority):
        self.priority = priority

    def setSuperTypes(self, super_type): 
        """Misschien is deze methode niet nodig, omdat de reasoner dit al moet doen"""
        self.super_types.extend(super_type)

    def setProperties(self):
        return self.properties
        
    def setAttendees(self, attendees):
        return self.attendees

    """ get class functions """
    def getName(self):
        return self.name

    def getType(self):
        return self.type
    
    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date

    def getTimeSlot(self):
        time_slot = [self.start_date, self.end_date]
        return time_slot

    def getPriority(self):
        return self.priority

    def getSuperTypes(self):
        return self.super_types

    def getProperties(self):
        return self.properties
        
    def getAttendees(self):
        return self.attendees
