
class UserInput():
    def __init__(self):
        self.creator_name = "NA"
        self.creator_email = "NA"
        self.appointment_name = "NA"
        self.type = "NA"
        self.start_date = None
        self.end_date = None
        self.priority = -1
        self.attendees = ["NA"]

    """set functions"""
    def setCreatorName(self, creator_name):
        self.creator_name = creator_name

    def setCreatorEmail(self, creator_email):
        self.creator_email = creator_email

    def setAppointmentName(self, appointment_name):
        self.appointment_name = appointment_name

    def setType(self, appointment_type):
        self.type = appointment_type

    def setStartDate(self, start_date):
        self.start_date = start_date

    def setEndDate(self, end_date):
        self.end_date = end_date

    def setPriority(self, priority_level):
        self.priority = priority_level
        
    def setAttendees(self, attendees):
        self.attendees = attendees

    """get functions"""
    def getCreatorName(self):
        return self.creator_name

    def getCreatorEmail(self):
        return self.creator_email

    def getAppointmentName(self):
        return self.appointment_name

    def getType(self):
        return self.type

    def getStartDate(self):
        return self.start_date

    def getEndDate(self):
        return self.end_date

    def getPriority(self, priority_level):
        return self.priority
        
    def getAttendees(self):
        return self.attendees


    