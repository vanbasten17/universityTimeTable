
class Classe:
    def __init__(self, summary, day, start_time, end_time, group, cr_type, room):
        self.summary = str(summary)
        self.day = str(day)
        self.start_time = str(start_time)
        self.end_time = str(end_time)
        self.group = str(group)
        self.cr_type = str(cr_type)
        self.room = str(room)

    def get_classe_information(self):
        print("\nCourse: " + self.summary)
        print("Day: " + self.day)
        print("Starts_at: " + self.start_time)
        print("Ends at: " + self.end_time)
        print("Group: " + self.group)
        print("Type: " + self.cr_type)
        print("Building: " + self.room + "\n")
