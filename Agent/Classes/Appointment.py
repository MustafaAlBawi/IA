
class Appointment():
    def __init__(self):
        #class properties (with __init__ value)
        self.appointment = None
        self.name = ""
        self.type = ""
        self.start_date = None
        self.end_date = None
        self.priority = -1
        self.super_types = []
        self.properties = []
        self.attendees = []

    def getAppointment(self):
        pass

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
