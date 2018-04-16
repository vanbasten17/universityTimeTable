from bs4 import BeautifulSoup
import re
from classes import Classe
import os


class Schedule_Scraper:
    months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
              'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

    day_codes = {'62px': '', '232px': '', '401px': '', '570px': '', '739px': ''}

    def __init__(self, schedules_directory):
        self.schedules_directory = schedules_directory
        self.files = []
        self.month = None
        self.week_info = []

    def load_classes_from_files(self):
        for filename in os.listdir(self.schedules_directory):
            if filename.endswith(".html"):
                relative_path = self.schedules_directory + "/" + filename
                soup_file = BeautifulSoup(open(relative_path, "r", encoding='utf-8', errors='ignore'), "html.parser")
                week_info = self.extract_information(soup_file)
                self.week_info.append(week_info)
        # return self.week_info #initial_month + list of week classes

    def extract_information(self, soup_file):
        month = self.extract_month(soup_file)
        week_days = self.extract_week_days(soup_file)
        print("initial month is: " + self.month)
        print("the week_days are: " + str(week_days))
        self.extract_classes(soup_file)
        return self.week_info

    def extract_month(self, soup_file):
        scraped_month = soup_file.find_all('h2')[1].get_text()  # months are in the h2 headers
        aux = []
        for k, v in self.months.items():
            if k in scraped_month:
                aux.append(str(v))
        self.month = min(aux)  # in case that there are more than one month, return the min

    def extract_week_days(self, soup_file):
        thead = soup_file.thead.get_text().split()
        del thead[0], thead[0], thead[5]
        week_days = []
        for item in thead:
            item = re.sub('\D', "", item)
            if len(str(item)) is 1:
                item = "0" + item
            week_days.append(item)
        self.associate_days_with_day_codes(week_days)
        return week_days

    def associate_days_with_day_codes(self, week_days):
        self.day_codes['62px'] = str(week_days[0])  # Monday
        self.day_codes['232px'] = str(week_days[1])  # Tuesday
        self.day_codes['401px'] = str(week_days[2])  # Wednesday
        self.day_codes['570px'] = str(week_days[3])  # Thursday
        self.day_codes['739px'] = str(week_days[4])  # Friday

    def extract_classes(self, file):
        classes = file.find("div", {"class": "fc-event-container"})  # find div with id = info-area
        # print(classes.prettify())
        for item in classes:
            aux = self.check_day(item)
            summary, start_time, end_time, group, cr_type, room = self.parse_classe(item.get_text())
            print(summary)
            print(start_time)
            print(end_time)
            print(group)
            print(cr_type)
            print(room)
            print("\n\n")

            # self.week_info.append(self.format_classe(classe))

    def check_day(self, item):
        aux = re.findall('(\w+)\s*: (\w+)', str(item))[2]
        positions = str(aux[1])
        if positions in self.day_codes:
            return self.day_codes.get(positions)

    def parse_classe(self, str_classe):
        # if 'Holiday' or 'No classes' in str_classe:
        #    return "Holiday / No classes", "00:00:00", "00:00:00", "", "", ""
        if False:
            print(" ")
        else:
            aux = str_classe.split("-")
            start_time = aux[0]
            end_time = re.search('(?:[01]\\d|2[0123]):(?:[012345]\\d)', aux[1]).group(0)
            course_info = aux[2]
            group = re.search('Group (.*?) ', course_info).group(0)
            summary = re.search('(.*?)Group', course_info).group(1).replace(" ", "", 1)
            course_info = aux[3]
            cr_type = re.search('(.*?)Classrooms', course_info).group(1).replace(" ", "")
            room = "No room assignated"

            if re.search('\\d+.\\d+', course_info) is not None:
                room = re.search('\\d+.\\d+', course_info).group(0)

        return summary, start_time, end_time, group, cr_type, room


'''
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
'''
