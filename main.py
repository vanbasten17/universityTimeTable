"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function

import datetime
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from schedule_scraper import Schedule_Scraper
import os

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))
default_calendar = 'primary'
dir_name = os.getcwd() + "/schedules"
year = '2018'  # TODO: Revisar aquesta bullshit
scraper = Schedule_Scraper(dir_name)
week_info = scraper.load_classes_from_files()
month = week_info[0]
classes = week_info[1]

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time


for classe in classes:
    start_time = year + "-" + month + "-" + classe.day + "T"+classe.start_time + "+02:00"
    end_time = year + "-" + month + "-" + classe.day + "T" + classe.end_time + "+02:00"
    event = {
        'summary': classe.summary + " : " + classe.cr_type + " " + classe.group,
        'location': classe.room,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Madrid',
        },
    }
    event = service.events().insert(calendarId=default_calendar, body=event).execute()
    #sino calendarId primary


