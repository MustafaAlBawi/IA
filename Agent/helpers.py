from Classes.UserInput import UserInput
from Classes.Appointment import Appointment
from Classes.Attendee import Attendee
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta, timezone
from dateutil import rrule
from owlready import *


def ConsoleGetUserInput():
    creator_name = input("What is your name?: ")
    creator_email = input("What is your gmail?: ")
    attendees = [(creator_name, creator_email)]

    appointment_name = input("What is the title of the appointment?: ")
    appointment_type = input("What is the type of the appointment? (See ontology for options): ")

    print("Next, what is the first potential date the appointment could be planned in for? \n \
        Could you first put the day of the month (nn), press enter, then month (mm), press enter, then the year (yyyy)?")
    start_day = input()
    start_month = input()
    start_year = input()

    print("Now, what is the first potential date the appointment could be planned in for? \n \
        Could you first put the day of the month (nn), press enter, then month (mm), press enter, then the year (yyyy)?")
    end_day = input()
    end_month = input()
    end_year = input()

    priority = input("What is the priority level of the appointment? (1-5): ")
    more_attendees = input("Are there more people, besides yourself, you'd like to invite to take part in the appointment? (y/n): ")
    
    if (more_attendees == "y"):
        amount_invitees = int(input("How many people would you like to invite?: "))
        for i in range(amount_invitees):
            name = input("What is the name of the person?: ")
            email = input("What is the email of the person?: ")
            attendees.append((name, email))
    
    start_date = datetime.date()
    start_date.day = int(start_day)
    start_date.month = int(start_month)
    start_date.year = int(start_year)

    end_date = datetime.date()
    end_date.day = int(end_day)
    end_date.month = int(end_month)
    end_date.year = int(end_year)
    

    """make UserInput variable with its properties"""
    user_input = UserInput()
    user_input.creator_name(creator_name)
    user_input.creator_email(creator_email)
    user_input.appointment_name(appointment_name)
    user_input.type(appointment_type)
    user_input.start_date(start_date)
    user_input.end_date(end_date)
    user_input.priority(int(priority))
    user_input.attendees(attendees)

    return user_input

    # print("Welcome to Time-Grasp; The app that creates appointments for you and your friends. \n \
    #         To make a new appointment, we need some information from you. \n \
    #         If you'd like to reset all input type \"restart\", \
    #         if you'd like to retype your last answer, type \"retype\".")
    
    # if (input == "restart"):
    #     pass
    # if (input == "retype"):
    #     pass

def createNewAppointment(user_input: UserInput):
    new_appointment = Appointment()
    new_appointment.setName(user_input.getName())
    new_appointment.setType(user_input.getType())
    new_appointment.setStartDate(user_input.getStartDate())
    new_appointment.setEndDate(user_input.getEndDate())
    new_appointment.setPriority(user_input.getPriority())
    # pas dit aan zodat t werkt (laat "appointment" weg zolang t niet gefikst is):
    new_.setSuperTypes("""get superTypes from ontology""")
    new_appointment.setAttendees(user_input.getAttendees())

    return new_appointment

def getPossibleTimeSlots(appointment: Appointment):
    event_times_priorities = [] # Array of array of tuples for possible timeslots;
    # check later for lowest_found_priority over all attendees

    type_time_slot = appointment.getTimeSlot() 
    start_date = appointment.getStartDate()
    end_date = appointment.getEndDate()
    attendees = appointment.getAttendees()

    days_between = (end_date - start_date).days # Days between start_date and end_date

    for attendee in attendees:
        potential_moments = [] # Array of time_slot tuples per attendee
        # For loop checks daily for possibilies
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            checkTimeSlots(day, type_time_slot, potential_moments)
        
        event_times_priorities.append(potential_moments)

    return event_times_priorities

def checkTimeSlots(day: datetime, time_slot: datetime, potentials_array: list):
    if day.weekday in time_slot: 
        """time_slot format moet nog worden gefikst, dus dit moet misschien nog worden aangepast"""
        """
            1. pak alle reeds ingeplande events op de dag day
            2. check of starttijden van events tussen start en eindtijd van te plannen appointment ligt
            3. zo ja: zet appointment starttijd en event-priority in respectievelijk in tuple
            4. zet alle appointment startijden zonder clash in tuple met priority = 0
            5. potentials_array.append(alle tuples)
        """
    else:
        break

def setEvent(appointment: Appointment, event_info): 
    # event_info is all additional data for the chosen event, besides the appointment data
    
    # calendarId = email addresses of attendees
    list_calenderIds = list()
    for iD in range(len(appointment.getAttendees())):
        list_calenderIds.append(appointment.attendees[iD].getEmail())


    new_event = Event {
        "end": {
    "dateTime": "",
    "date": "",
    "timeZone": ""
    },
    "start": {
        "date": "",
        "dateTime": "",
        "timeZone": ""
    },
    "attendees": []
    }










