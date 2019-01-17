from owlready2 import *
import numpy as np
from random import randint

onto = get_ontology('./Agent/Resources/Ontology/AppointmentTypes3.owl')
onto.load()

class Appointment:
    def __init__(self, name = "", type_ = "", start_date = None, end_date = None, priority=-1, amount_to_plan = 1, duration = 1, attendees = []):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.priority = int(priority)
        self.amount = int(amount_to_plan)
        self.duration = int(duration)
        self.attendees = attendees
        self.time_slots = []

        if type_ != "":
            if (type_ == "Friends" or type_ == "Colleagues" or type_ == "Family"):
                instances_with_people = onto.search(withPeople=onto[type_])
                random_int = int(randint(0, len(instances_with_people) - 1))

                self.type = instances_with_people[random_int]
            else:
                self.type = type_
        else:
            with_people = ["Friends", " Colleagues", "Family"]
            people_type = with_people[int(randint(0,2))]
            instances_with_people = onto.search(withPeople=onto[people_type])
            random_int = int(randint(0, len(instances_with_people) - 1))

            self.type = instances_with_people[random_int]

    def getTimesWithPeople(self):
        if (self.type != "Friends" or self.type != "Colleagues" or self.type != "Family"):
            instances_with_people = onto.search(withPeople=onto[self.type].withPeople)
            people_times = []

            for _type in instances_with_people:
                people_times.extend(_type.hasTime)

            return people_times
        else:
            instances_with_people = onto.search(withPeople=onto[self.type])
            people_times = []

            for _type in instances_with_people:
                people_times.extend(_type.hasTime)

            return people_times

    def getRandomType(self, people_type):
        instances_with_people = onto.search(withPeople=onto[people_type])
        random_int = int(randint(0, len(instances_with_people)-1))

        return instances_with_people[random_int]
        

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

    def getDayParts(self):
        type_day_parts = []

        if onto["Night"] in onto[self.type].hasPartofDay:
            type_day_parts.extend([0,1,2,3,4,5])
        if onto["Morning"] in onto[self.type].hasPartofDay:
            type_day_parts.extend([6,7,8,9,10,11])
        if onto["Afternoon"] in onto[self.type].hasPartofDay:
            type_day_parts.extend([12,13,14,15,16,17])
        if onto["Evening"] in onto[self.type].hasPartofDay:
            type_day_parts.extend([18,19,20,21,22,23])

        return type_day_parts    
        
    def getAttendees(self):
        return self.attendees
