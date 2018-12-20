# -*- coding: utf-8 -*-

"""

"""
import helpers
from Classes.Test import Test
from Classes.GoogleCalendar import GoogleCalendar

"""Start the App"""

def start():
        GC = GoogleCalendar('readonly')
        events = GC.events('primary', GC.now, 10, True, 'startTime')\
            .get('items', [])
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])