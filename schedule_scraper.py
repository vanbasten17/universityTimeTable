from bs4 import BeautifulSoup
import os
import codecs
import calendar
import re
from classes import Classe

class Schedule_Scraper:
    months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 
                'July': '07', 'August': '08','September': '09','October': '10','November': '11' ,'December': '12'}
    
    days = {62:'', 232:'', 401:'',570:'',739:''}

    def __init__(self, schedule_directory):
        self.schedule_directory = schedule_directory
        self.init_files()
    
    def init_files(self):
        self.files = []
        for filename in self.schedule_directory:
                if filename.endswith(".html"): 
                    soup_file = BeautifulSoup(open(filename, "r", encoding="utf-8", errors = "ignore"), "html.parser")
                    self.files.append(soup_file)
    
    def scrap_files(self):
        for file in self.files:
            month = self.extract_month(file)
            week_days = self.extract_week_days(file)
            print("the month is: " + month)
            print("the week_days are: " + str(week_days))
            self.associate_days_with_codes(week_days)
            print(self.days)
            self.extract_classes(file)
        return self.week_info


    def extract_month(self, file):
        scraped_month = file.find_all('h2')[1].get_text() #months are in the h2 headers
        for k,v in self.months.items():
          if k in scraped_month:
            return str(v) #contains the digit of the month #gestionar si es p.ex. may-april
    
    def extract_week_days(self, file):
        thead = file.thead.get_text().split()
        del thead[0], thead[0], thead[5]
        week_days = []
        for item in thead:
          item = re.sub('\D', "", item)
          if len(str(item)) is 1:
            item = "0" + item
          week_days.append(item)
        return week_days

    def associate_days_with_codes(self, week_days):
        self.days[62] = week_days[0]
        self.days[232] = week_days[1]
        self.days[401] = week_days[2]
        self.days[570] = week_days[3]
        self.days[739] = week_days[4]

    def extract_classes(self, file):
        classes = file.find("div", {"class": "fc-event-container"}) #find div with id = info-area    
        self.week_info = [] 
        for item in classes:
          #print(item.get_text())
          self.week_info.append((str(self.check_day(item)) + " " + item.get_text()))

    def check_day(self, item):
        aux = re.findall('(\w+)\s*: (\w+)', str(item))[2]
        positions = int(aux[1][:-2])
        return positions
