# Alex Ramey (abr8xq)

# read_input.py is intended to serve as the interface between the raw data
# and process_input.py. This means that changes to input format should only
# affect this file, which is responsible for providing process_input.py with a
# list of Student objects and a list of Teacher objects.

import csv

class Student:
    def __init__(self, student_id, is_returner, school_preference, teacher_preference, time_slot_ids, is_driver, num_seats):
        self.student_id = student_id.strip()
        self.is_returner = is_returner
        self.num_seats = num_seats
        self.is_driver = is_driver
        # TODO: We need unique school and teacher_ids
        self.school_preference = school_preference.strip()
        self.teacher_preference = teacher_preference.strip()
        self.time_slot_ids = time_slot_ids

    def __repr__(self):
        #return self.student_id
        return self.student_id + " " + str(self.time_slot_ids)

    def __eq__(self, other):
        if isinstance(other, Student):
            return (self.student_id == other.student_id)
        else:
            return False
    def __hash__(self):
        return hash(self.student_id)

class Teacher:
    def __init__ (self, teacher_name, teacher_school, time_slot_ids):
        self.teacher_name = teacher_name.strip()
        # TODO: We need unique school and teacher_ids
        self.teacher_school = teacher_school.strip()
        self.teacher_id = self.teacher_school + self.teacher_name
        self.time_slot_ids = time_slot_ids

    def __repr__(self):
        return self.teacher_id
        #return self.teacher_id + " " + str(self.time_slot_ids)

    def __eq__(self, other):
        if isinstance(other, Teacher):
            return (self.teacher_id == other.teacher_id)
        else:
            return False

    def __hash__(self):
        return hash(self.teacher_id)

def readInStudentsFile():
    students = []
    with open('STUDENTS.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            is_driver = (row[3] == 'Yes')
            num_seats = int(row[4])
            is_returner = (row[10] == 'Yes')
            school_preference = row[11]
            teacher_preference = row[12]
            time_slot_ids = generateListOfTimeIntervalIDs(row[5], row[6], row[7], row[8], row[9], True)
            students.append(Student(row[1], is_returner, school_preference, teacher_preference, time_slot_ids, is_driver, num_seats))
    return list(set(students))

def readInTeachersFile():
    teachers = []
    with open('TEACHERS.csv', newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            teacher_name = row[1]
            teacher_school = row[3]
            time_slot_ids = generateListOfTimeIntervalIDs(row[7],row[8],row[9],row[10],row[11], False)
            teachers.append(Teacher(teacher_name, teacher_school, time_slot_ids))
    return list(set(teachers))

def generateListOfTimeIntervalIDs(monday_list, tuesday_list, wednesday_list, thursday_list, friday_list, is_thirty_min_intervals):
    """ Parse weekday availabilities and return one long list with unique time_slot_ids.
        time_slot_ids indicate one-hour availability chunks and range from 1 - 239,
        where 1 represents 12am - 1am Monday morning, 2 represents 12:30am - 1:30am
        Monday morning . . . 239 represents 11pm-midnight on Friday """

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
                # guard against case of empty string i.e. no intervals for some weekday
                if (interval != ''):
                    interval_components = interval.split('-')
                    reverse_interval = interval_components[1] + '-' + interval_components[0]
                    # This is guaranteed to succeed and return time_slot_id for start of interval
                    time_interval_ids.append(offset + get_slot_id(interval, reverse_interval))

    return time_interval_ids

def get_slot_id(interval1, interval2):
    interval1Times = interval1.split('-')
    interval2Times = interval2.split('-')

    if (len(interval1Times) != 2 or len(interval2Times) != 2 or interval1Times[1].strip() != interval2Times[0].strip()):
        return -1
    else:
        # we have an hour-long block
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

if __name__ == '__main__':
    students = readInStudentsFile()
    print(students)
    teachers = readInTeachersFile()
    print(teachers)

    #test for duplicates . . .
    dups = []
    for x in range(0, len(students)):
        for i in range(x+1, len(students)):
            if students[x].student_id == students[i].student_id and students[x].student_id not in dups:
                dups.append(students[x].student_id)
    for x in range(0, len(teachers)):
        for i in range(x+1, len(teachers)):
            if teachers[x].teacher_id == teachers[i].teacher_id and teachers[x].teacher_id not in dups:
                dups.append(teachers[x].teacher_id)

    print(dups)