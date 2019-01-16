
class Attendee():
    def __init__(self, name, email, id_number):
        self.name = name
        self.email = email
        self.priority = None
        self.id = id_number

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email

    def getPriority(self):
        return self.priority

    def getID(self):
        return self.id