# Alex Ramey (abr8xq)

# read_input.py is intended to serve as the interface between the raw data
# and process_input.py. This means that changes to input format should only
# affect this file, which is responsible for providing process_input.py with a
# list of Student objects and a list of Teacher objects.

import csv

g_students_csv = 'STUDENTS.csv'
g_teachers_csv = 'TEACHERS.csv'

class Student:
    def __init__(self, student_id, first_name, last_name,
                 major, year, phone_number, is_driver, num_passenger_seats,
                 is_returner, preference, time_slot_ids):
        self.student_id = student_id.strip().replace('_','')
        self.name = first_name.strip() + " " + last_name.strip()
        self.major = major.strip()
        self.year = str(year).strip()
        self.phone_number = str(phone_number).strip()
        self.is_driver = is_driver
        self.num_passenger_seats = int(num_passenger_seats)
        self.is_returner = is_returner
        self.school_preference = preference.strip()
        self.time_slot_ids = set(time_slot_ids)
        self.car_assignment = None
        self.time_assignment = None

    def __repr__(self):
        return self.student_id
        #return self.student_id + " " + str(self.time_slot_ids)

    def __eq__(self, other):
        if isinstance(other, Student):
            return (self.student_id == other.student_id)
        else:
            return False

    def __hash__(self):
        return hash(self.student_id)

class Teacher:
    def __init__ (self, teacher_email, first_name, last_name,
                  school_id, room_number, grade_level, subjects,
                  max_num_helpers_at_once, max_num_helpers_per_week,
                  special_message, time_slot_ids):
        self.email = teacher_email.strip()
        self.name = first_name.strip() + " " + last_name.strip()
        self.teacher_school = school_id.strip()
        self.room_number = str(room_number).strip()
        self.grade_level = str(grade_level).strip()
        self.subjects = subjects.strip()
        self.max_num_helpers_per_week = int(max_num_helpers_per_week)
        self.max_num_helpers_at_once = min(int(max_num_helpers_at_once), self.max_num_helpers_per_week)
        self.special_message = special_message.strip()
        self.time_slot_ids = set(time_slot_ids)

        # used to track teacher assignments
        self.num_helpers_assigned = 0
        self.assigned_time_slot_ids = {}    # a dictionary mapping time_slots to num_helpers_assigned

    def __repr__(self):
        return self.email
        #return self.email + " " + str(self.time_slot_ids)

    def __eq__(self, other):
        if isinstance(other, Teacher):
            return (self.email == other.email)
        else:
            return False

    def __hash__(self):
        return hash(self.email)

def readInStudentsFile():
    students = []
    with open(g_students_csv, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time_slot_ids = generateListOfTimeIntervalIDs(row[10], row[11], row[12], row[13], row[14], True)
            students.append(Student(row[0], row[1], row[2], row[3], row[4], row[5], (row[6]=='Yes'), row[7], (row[8] == 'Yes'), row[9], time_slot_ids))
    return list(set(students))

def readInTeachersFile():
    teachers = []
    with open(g_teachers_csv, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time_slot_ids = generateListOfTimeIntervalIDs(row[10],row[11],row[12],row[13],row[14], False)
            teachers.append(Teacher(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], time_slot_ids))
    return list(set(teachers))


"""
Parse weekday availabilities and return one long list of unique interger time_slot_ids.
time_slot_ids indicate one-hour availability chunks and range from 0 - 239,
where 0 represents 12am - 1am Monday morning, 2 represents 12:30am - 1:30am
Monday morning . . . 239 represents 11:30pm (on Friday) - 12:30 a.m. Saturday
"""
def generateListOfTimeIntervalIDs(monday_list, tuesday_list, wednesday_list, thursday_list, friday_list, is_thirty_min_intervals):
    monday_times = monday_list.split(',')
    tuesday_times = tuesday_list.split(',')
    wednesday_times = wednesday_list.split(',')
    thursday_times = thursday_list.split(',')
    friday_times = friday_list.split(',')

    interval_lists = [monday_times, tuesday_times, wednesday_times, thursday_times, friday_times]
    time_interval_ids = []

    for i in range(0,len(interval_lists)):
        offset = i * 48
        if (is_thirty_min_intervals):
            # Student Time Intervals
            for j in range (0, len(interval_lists[i]) - 1):
                slot_id = get_slot_id(interval_lists[i][j], interval_lists[i][j+1])
                if (slot_id != -1):
                    time_interval_ids.append(offset + slot_id)
        else:
            # Teacher Time Intervals
            for interval in interval_lists[i]:
                if (interval.strip() != ''):
                    interval_components = interval.split('-')
                    # a trick to make get_slot_id() work for a single hour long interval
                    # instead of two half hours ones
                    reverse_interval = interval_components[1] + '-' + interval_components[0]
                    time_interval_ids.append(offset + get_slot_id(interval, reverse_interval))

    return time_interval_ids

"""
Given two intervals (assumed to be 30 minutes long), we check that the second
interval begins when the first one ends. If the input is valid and this is the
case, then we only focus on the start of the first interval, and translate this
start_time into an integer in the range 1-239. Returns -1 on failure.
"""
def get_slot_id(interval1, interval2):
    interval1Times = interval1.split('-')
    interval2Times = interval2.split('-')

    if (len(interval1Times) != 2 or len(interval2Times) != 2 or interval1Times[1].strip() != interval2Times[0].strip()):
        return -1
    else:
        slot_id = 0
        if ('pm' in interval1Times[0]):
            slot_id += 24
        start_hour_min = interval1Times[0].strip().split(':')
        if (int(start_hour_min[0]) == 12):
            start_hour_min[0] = '0'
        slot_id += 2 * int(start_hour_min[0])
        if (int((start_hour_min[1])[0:2]) == 30):
            slot_id += 1
        return slot_id
"""
if __name__ == '__main__':
    students = readInStudentsFile()
    print(students)
    teachers = readInTeachersFile()
    print(teachers)
"""