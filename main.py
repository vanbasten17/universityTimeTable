"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from schedule_scraper import Schedule_Scraper
from bs4 import BeautifulSoup
import os
import codecs
import calendar
import re

dir_name = "/home/marc/Escriptori/HorariUni"
directory = os.listdir(dir_name)
scraper = Schedule_Scraper(directory)
week_info = scraper.scrap_files()


# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
#now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
for item in week_info:

  event = {
    'summary': str(item),
    'location': 'room',
    'description': 'group',
    'start': {
      'dateTime': '2018-05-28T09:00:00-07:00',
      'timeZone': 'Europe/Madrid',
    },
    'end': {
      'dateTime': '2018-05-28T17:00:00-07:00',
      'timeZone': 'Europe/Madrid',
    },
  }
  #event = service.events().insert(calendarId='primary', body=event).execute()