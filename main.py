"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
import numpy as np
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

i = 0
for classe in enumerate(classes):
    #print(classe[1])
    if i < len(classes)-1:
        if classes[i+1][1] < classes[i][1]:
            month = str("0" + str(int(month)+1))
        i += 1
    aux = classe[1]
    summary = aux[0]
    day = aux[1]
    start_time = aux[2]
    end_time = aux[3]
    group = aux[4]
    cr_type = aux[5]
    room = aux[6]
    start_time = year + "-" + month + "-" + day + "T"+ start_time + "+02:00"
    end_time = year + "-" + month + "-" + day + "T" + end_time + "+02:00"
    event = {
        'summary': summary + " : " + cr_type + " " + group,
        'location': room,
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


