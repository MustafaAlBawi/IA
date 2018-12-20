
class Attendee():
    def __init__(self, name, email, priority):
        self.name = name
        self.email = email
        self.priority = priority

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email

    def getPriority(self):
        return self.priority