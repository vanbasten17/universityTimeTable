"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function


from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from schedule_scraper import Schedule_Scraper
import os

dir_name = os.getcwd() + "/schedules"
year = '2018'  # TODO: Revisar aquesta bullshit
scraper = Schedule_Scraper(dir_name)
week_info = scraper.load_classes_from_files()

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

print("")
# start_time = str(year + '-' + item.month + '-' + item.day[:-1] + 'T' + item.start_time[:-1] + ":00" + '+02:00')
# end_time = str(year + '-' + item.month + '-' + item.day[:-1] + 'T' + item.end_time +  ":00" + '+02:00')
'''event = {
'summary': str(item.course),
'location': str(item.room),
'start': {
'dateTime': start_time,
'timeZone': 'Europe/Madrid',
},
'end': {
'dateTime': end_time,
'timeZone': 'Europe/Madrid',
    },
  }'''
    # event = service.events().insert(calendarId='primary', body=event).execute()
