


class Event(object):
    def __init__(self, owner = None, priority = 1):
        self.owners_priorities = [owner, priority]
        self.highest = priority

    def add_owner(self, owner = None, priority = 1):
        if self.highest < priority:
            self.highest = priority
            
        self.owners_priorities = self.owners_priorities.extend([owner, priority])

    def getOwnersPriorities(self):
        return self.owners_priorities
    
    def getHighest(self):
        return self.highest








