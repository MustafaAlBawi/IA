from Classes.UserInput import UserInput
import datetime


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



    # print("Welcome to Time-Grasp; The app that creates appointments for you and your friends. \n \
    #         To make a new appointment, we need some information from you. \n \
    #         If you'd like to reset all input type \"restart\", \
    #         if you'd like to retype your last answer, type \"retype\".")
    
    # if (input == "restart"):
    #     pass
    # if (input == "retype"):
    #     pass

    



