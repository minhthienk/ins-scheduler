
import math
import itertools
import numpy as np
from datetime import date




class InsClass():
    """docstring for InsClass"""
    KID_LESSON_NUMBER = 25
    TEEN_LESSON_NUMBER = 35
    SMARTCHOICE_NATIVE_RATE = 70
    REGULAR_NATIVE_RATE = 20

    SMARTCHOICE_VN_RATE = 100 - SMARTCHOICE_NATIVE_RATE
    REGULAR_VN_RATE = 100 - REGULAR_NATIVE_RATE
    class_dict = {}
    def __init__(self, 
            class_name, 
            teacher, 
            time_frames, 
            native_lesson_count, 
            main_vn_teacher_lesson_count):

        self.class_name = class_name
        self.start_date = self.class_name[-6:]
        self.time_frames = time_frames
        self.week_num = self.get_week_num()
        self.native_lesson_count = native_lesson_count
        self.main_vn_teacher_lesson_count = main_vn_teacher_lesson_count
        self.learned_lessons_number = self.count_learned_lessons()

        self.native_lesson_count_temp = native_lesson_count
        self.main_vn_teacher_lesson_count_temp = main_vn_teacher_lesson_count
        self.learned_lessons_number_temp = self.count_learned_lessons()
        self.native_learned = False # this flag is used to mark if there is native teacher in this class this week
        self.teacher = teacher

        self.native_learned_set=False
        InsClass.class_dict[self.class_name] = self


    def get_native_need_rate(self):
        # regular classes do not need a native if learnedlesson number <= 5
        if self.class_name.startswith('SK') or self.class_name.startswith('SB') or \
                self.class_name.startswith('ST') or self.class_name.startswith('SL'):
            if self.learned_lessons_number_temp <= 5: 
                return 100
            if self.native_learned==True:
                return 100
        # calcualte native need rate based on class type
        if self.class_name.startswith('SCA'):
            return ((self.native_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_NATIVE_RATE
        if self.class_name.startswith('SCB'):
            return ((self.native_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_NATIVE_RATE
        if self.class_name.startswith('SK') or self.class_name.startswith('SB') :
            return ((self.native_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_NATIVE_RATE
        if self.class_name.startswith('ST') or self.class_name.startswith('SL') or self.class_name.startswith('IE'):
            return ((self.native_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_NATIVE_RATE
        

    def get_main_vn_teacher_need_rate(self):
        # smartchoice classes do not need a vn if learnedlesson number <= 5
        if self.class_name.startswith('SC'):
            if self.learned_lessons_number_temp <= 5: 
                return 100
        # calcualte vn need rate based on class type
        if self.class_name.startswith('SCA'):
            return ((self.main_vn_teacher_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_VN_RATE
        if self.class_name.startswith('SCB'):
            return ((self.main_vn_teacher_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_VN_RATE
        if self.class_name.startswith('SK') or self.class_name.startswith('SB') :
            return ((self.main_vn_teacher_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_VN_RATE
        if self.class_name.startswith('ST') or self.class_name.startswith('SL') or self.class_name.startswith('IE'):
            return ((self.main_vn_teacher_lesson_count_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_VN_RATE

    def increase_native_lesson_count(self):
        self.native_lesson_count_temp += 1
        # regular classes do not need a native if learnedlesson number <= 5
        if self.class_name.startswith('SK') or self.class_name.startswith('SB') or \
                self.class_name.startswith('ST') or self.class_name.startswith('SL'):
            self.native_learned = True

    def increase_main_vn_teacher_lesson_count(self):
        self.main_vn_teacher_lesson_count_temp += 1

    def increase_learned_lesson_number(self):
        self.learned_lessons_number_temp +=1

    def reset_lesson_numbers(self):
        self.native_lesson_count_temp = self.native_lesson_count
        self.main_vn_teacher_lesson_count_temp = self.main_vn_teacher_lesson_count
        self.learned_lessons_number_temp = self.learned_lessons_number 
        if self.native_learned_set==True:
            self.native_learned = True # assign rooif cos reset k
        else:
            self.native_learned = False

    def update_lesson_numbers(self):
        self.native_lesson_count = self.native_lesson_count_temp
        self.main_vn_teacher_lesson_count = self.main_vn_teacher_lesson_count_temp
        self.learned_lessons_number = self.learned_lessons_number_temp
        if self.native_learned==True:
            self.native_learned_set==True




    def count_learned_lessons(self):
        # get year month day from class code
        year = '20' + self.start_date[-2:]
        month = self.start_date[2:4]
        day = self.start_date[:2]

        # calculate that day and today
        thatday = year + '-' + month + '-' + day
        today = str(date.today())
        today = ('2021-02-01') # check this day to use the data

        total_count = 0
        for lesson_time in self.time_frames:
            processing_weekday = lesson_time[:3].capitalize()
            total_count += np.busday_count(thatday, today, weekmask=processing_weekday)
        
        return total_count

    def get_week_num(self):
        # get year month day from class code
        year = int('20' + self.start_date[-2:])
        month = int(self.start_date[2:4])
        day = int(self.start_date[:2])

        # convert startday and today to date object
        that_day = date(year, month, day)
        today = date.today()

        # calculate number of days gone by
        delta = today - that_day
        day_num = delta.days+1

        # calcuate start weekday
        start_weekday = that_day.weekday()

        # 2 cases: start day is on Monday and else
        if start_weekday==0:
            week_num = math.ceil(day_num/7)
        else:
            week_num = 1 + math.ceil((day_num-(7-start_weekday))/7)

        return week_num





class Teacher():
    """docstring for Teacher"""
    teacher_dict = {}
    def __init__(self, name, teacher_type,
            predefined_days_off,
            number_days_off,
            improper_class_names,):

        self.name = name 
        self.improper_class_names = improper_class_names
        self.predefined_days_off = predefined_days_off
        self.type = teacher_type
        self.number_days_off = number_days_off
        self.lesson_count = 0 # number of lessons this teacher have taught
        self.lesson_count_temp = 0
        # use this var to check if 
        Teacher.teacher_dict[self.name] = self


    def get_days_off_possibilities(self):
        number_of_more_days_off = self.number_days_off - len(self.predefined_days_off)

        if 'parttime' in self.type:
            return []

        possibilities = []
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        weekdays = [self.name + '-' + day for day in weekdays]

        predefined_days_off = [self.name + '-' + day for day in self.predefined_days_off]

        days_left = set(weekdays) - set(predefined_days_off)
        for subset in itertools.combinations(days_left, number_of_more_days_off):
            subset = list(subset)
            subset.extend([self.name + '-' + day for day in self.predefined_days_off])
            possibilities.append(subset)
        return(possibilities)




def get_teacher_by_name(teacher_name):
    if teacher_name in Teacher.teacher_dict.keys():
        return Teacher.teacher_dict[teacher_name]
    else:
        return None

def get_class_by_name(class_name):
    return InsClass.class_dict[class_name]

def get_teacher_main_classes(teacher):
    classes = []
    for cl in InsClass.class_dict.values():
        if cl.teacher is teacher:
            classes.append(cl)
    return classes
# to do: cac truong hop sai du lieu, sai ten lop, sai ten gv