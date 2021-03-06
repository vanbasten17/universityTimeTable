from bs4 import BeautifulSoup
import re
from classes import Classe
import os


class Schedule_Scraper:
    months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
              'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

    day_codes = {}

    def __init__(self, schedules_directory):
        self.schedules_directory = schedules_directory
        self.files = []
        self.month = None
        self.week_classes = []

    def load_classes_from_files(self):
        for filename in os.listdir(self.schedules_directory):
            if filename.endswith(".html"):
                relative_path = self.schedules_directory + "/" + filename
                soup_file = BeautifulSoup(open(relative_path, "r", encoding='utf-8', errors='ignore'), "html.parser")
                week_info = self.extract_information(soup_file)
                return (self.month, week_info);


    def extract_information(self, soup_file):
        month = self.extract_month(soup_file)
        week_days = self.extract_week_days(soup_file)

        #print("initial month is: " + self.month)
        #print("the week_days are: " + str(week_days))
        self.extract_classes(soup_file)
        #for item in self.week_classes:
        #    print(item.summary, item.day)
        return self.week_classes

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
        self.day_codes['230px'] = str(week_days[1])  # Tuesday
        self.day_codes['401px'] = str(week_days[2])  # Wednesday
        self.day_codes['397px'] = str(week_days[2])  # Wednesday
        self.day_codes['570px'] = str(week_days[3])  # Thursday
        self.day_codes['564px'] = str(week_days[3])  # Thursday
        self.day_codes['731px'] = str(week_days[4])  # Friday
        self.day_codes['739px'] = str(week_days[4])  # Friday
        # 54, 98, 145, 210, 263
        # 62, 141, 219, 297, 375
        # 62, 178, 293, 408, 523

    def extract_classes(self, file):
        classes = file.find("div", {"class": "fc-event-container"})  # find div with id = info-area
        # print(classes.prettify())
        for item in classes:
            day = self.check_day(item)
            summary, start_time, end_time, group, cr_type, room = self.parse_classe(item.get_text())
            #print(summary, start_time, end_time, group, cr_type, room)
            classe = ();
            classe = (summary, day, start_time, end_time, group, cr_type, room);
            #    def __init__(self, summary, day, start_time, end_time, group, cr_type, room): constructor of classe
            self.week_classes.append(classe)

    def check_day(self, item):
        aux = re.findall('(\w+)\s*: (\w+)', str(item))[2]
        positions = str(aux[1])
        if positions in self.day_codes:
            return self.day_codes.get(positions)

    def parse_classe(self, str_classe):
        #print(str_classe)
        if 'Holiday' in str_classe:
            return "Holiday", "00:00:00", "00:00:00", "", "", ""
        else:
            aux = str_classe.split("-")
            start_time = aux[0].replace(" ", "") + ":00"
            end_time = re.search('(?:[01]\\d|2[0123]):(?:[012345]\\d)', aux[1]).group(0) + ":00"
            course_info = aux[2]
            group = re.search('Group (.*?) ', course_info).group(0)
            summary = re.search('(.*?)Group', course_info).group(1).replace(" ", "", 1)
            course_info = aux[3]
            cr_type = re.search('(.*?)Classrooms', course_info).group(1).replace(" ", "")
            room = "No room assignated"

            if re.search('\\d+.\\d+', course_info) is not None:
                room = re.search('\\d+.\\d+', course_info).group(0)

            return summary, start_time, end_time, group, cr_type, room
