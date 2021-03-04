from datetime import date
import math

import sys
import itertools

import time
import numpy as np

data = [['SK1B1-121220', 'Ms.Mia', ['sat-08h00-09h30', 'sun-08h00-09h30'], 3, 13],
['SK1P2-201220', 'Ms.Jay', ['sat-08h00-09h30', 'sun-08h00-09h30'], 3, 9],
['SK1A3-271220', 'Ms.Amy', ['sat-08h00-09h30', 'sun-08h00-09h30'], 2, 9],
['SCA2A3-271220', 'Mr.Andre', ['sat-09h50-11h20', 'sun-09h50-11h20'], 8, 8],
['SK2B4-100121', 'Ms.Jay', ['sat-09h50-11h20', 'sun-09h50-11h20'], 1, 6],
['SK2M3-030121', 'Mr.Noland', ['sat-09h50-11h20', 'sun-09h50-11h20'], 1, 8],
['SK4B1-020121', 'Ms.Mia', ['sat-09h50-11h20', 'sun-09h50-11h20'], 1, 9],
['ST3B4-180121', 'Ms.Amy', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 1, 5],
['ST3D2-041220', 'Ms.Jay', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 3, 19],
['ST4C2-021220', 'Mr.Kay', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 4, 19],
['ST2G2-231120', 'Ms.Phúc', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 4, 21],
['SB3E1-131120', 'Mr.Noland', ['wed-17h40-19h10', 'fri-17h40-19h10'], 2, 14],
['SK2K4-211220', 'Ms.Jane', ['mon-17h40-19h10', 'wed-17h40-19h10'], 2, 9],
['SK1O3-060121', 'Ms.Jenni', ['mon-17h40-19h10', 'wed-17h40-19h10'], 2, 5],
['SL2G4-181220', 'Ms.Jay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 3, 14],
['ST2H1-161120', 'Ms.Mia', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 2, 25],
['SL3F1-111120', 'Ms.Jane', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 2, 29],
['SL1A2-071220', 'Ms.Jenni', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 1, 20],
['IE3A1-251120', 'Mr.Kay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 5, 21],
['SK2N1-071120', 'NoTeacher', ['wed-17h40-19h10', 'sat-17h40-19h10'], 2, 0],
['SCB2A2-291220', 'Mr.Matt', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 15, 15],
['SK3E2-160121', 'Ms.Jay', ['tue-17h40-19h10', 'sat-17h40-19h10'], 0, 5],
['SB4C1-191120', 'Ms.Amy', ['tue-17h40-19h10', 'thu-17h40-19h10'], 0, 17],
['ST1E2-211120', 'Ms.Jane', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 4, 24],
['ST2F4-171220', 'Ms.Mia', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 2, 16],
['SCB3B3-081220', 'Mr.Matt', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 18, 18],
['SL3B4-101120', 'Ms.Jane', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 6, 23],
['ST1A3-210121', 'Ms.Amy', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 1, 4]]







class InsClass():
    """docstring for InsClass"""
    KID_LESSON_NUMBER = 25
    TEEN_LESSON_NUMBER = 35
    SMARTCHOICE_NATIVE_RATE = 70
    REGULAR_NATIVE_RATE = 20

    SMARTCHOICE_VN_RATE = 100 - SMARTCHOICE_NATIVE_RATE
    REGULAR_VN_RATE = 100 - REGULAR_NATIVE_RATE

    def __init__(self, class_code, lesson_times, native_lesson_number, main_vn_teacher_lesson_number):
        self.class_code = class_code
        self.start_date = self.class_code[-6:]
        self.lesson_times = lesson_times
        self.week_num = self.get_week_num()
        self.native_lesson_number = native_lesson_number
        self.main_vn_teacher_lesson_number = main_vn_teacher_lesson_number
        self.learned_lessons_number = self.count_learned_lessons()

        self.native_lesson_number_temp = native_lesson_number
        self.main_vn_teacher_lesson_number_temp = main_vn_teacher_lesson_number
        self.learned_lessons_number_temp = self.count_learned_lessons()

    def get_native_need_rate(self):
        # regular classes do not need a native if learnedlesson number <= 5
        if self.class_code.startswith('SK') or self.class_code.startswith('SB') or \
                self.class_code.startswith('ST') or self.class_code.startswith('SL'):
            if self.learned_lessons_number_temp <= 5: 
                return 100

        # calcualte native need rate based on class type
        if self.class_code.startswith('SCA'):
            return ((self.native_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_NATIVE_RATE
        if self.class_code.startswith('SCB'):
            return ((self.native_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_NATIVE_RATE
        if self.class_code.startswith('SK') or self.class_code.startswith('SB') :
            return ((self.native_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_NATIVE_RATE
        if self.class_code.startswith('ST') or self.class_code.startswith('SL') or self.class_code.startswith('IE'):
            return ((self.native_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_NATIVE_RATE
        
    def get_main_vn_teacher_need_rate(self):
        # smartchoice classes do not need a vn if learnedlesson number <= 5
        if self.class_code.startswith('SC'):
            if self.learned_lessons_number_temp <= 5: 
                return 100

        # calcualte vn need rate based on class type
        if self.class_code.startswith('SCA'):
            return ((self.main_vn_teacher_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_VN_RATE
        if self.class_code.startswith('SCB'):
            return ((self.main_vn_teacher_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.SMARTCHOICE_VN_RATE
        if self.class_code.startswith('SK') or self.class_code.startswith('SB') :
            return ((self.main_vn_teacher_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_VN_RATE
        if self.class_code.startswith('ST') or self.class_code.startswith('SL') or self.class_code.startswith('IE'):
            return ((self.main_vn_teacher_lesson_number_temp*100)/self.learned_lessons_number_temp)*100/InsClass.REGULAR_VN_RATE



    def increase_native_lesson_number(self):
        self.native_lesson_number_temp += 1

    def increase_main_vn_teacher_lesson_number(self):
        self.main_vn_teacher_lesson_number_temp += 1

    def increase_learned_lesson_number(self):
        self.learned_lessons_number_temp +=1

    def reset_lesson_numbers(self):
        self.native_lesson_number_temp = self.native_lesson_number
        self.main_vn_teacher_lesson_number_temp = self.main_vn_teacher_lesson_number
        self.learned_lessons_number = self.count_learned_lessons()

    def count_learned_lessons(self):
        # get year month day from class code
        year = '20' + self.start_date[-2:]
        month = self.start_date[2:4]
        day = self.start_date[:2]

        # calculate that day and today
        thatday = year + '-' + month + '-' + day
        today = str(date.today())

        total_count = 0
        for lesson_time in self.lesson_times:
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
    def __init__(self, name, type='vnfulltime', 
            main_classes=None,
            improper_classes=None,
            predefined_days_off=None,
            number_of_off_days=1):

        #set teacher name
        self.name = name

        # classes that the teacher can not teach
        if main_classes==None:
            self.main_classes = []
        else:
            self.main_classes = main_classes

        # classes that the teacher can not teach
        if improper_classes==None:
            self.improper_classes = []
        else:
            self.improper_classes = improper_classes

        # days that the teacher have asks for being off
        if predefined_days_off==None:
            self.predefined_days_off = []
        else:
            self.predefined_days_off = predefined_days_off

        # teacher type: vnfulltime, vnparttime, ntfulltime, ntparttime
        self.type = type
        self.number_of_off_days = number_of_off_days

    def get_days_off_possibilities(self):
        number_of_more_days_off = self.number_of_off_days - len(self.predefined_days_off)


        if 'parttime' in self.type:
            return []

        possibilities = []
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        weekdays = [self.name + '-' + day for day in weekdays]
        days_left = set(weekdays) - set(self.predefined_days_off)
        for subset in itertools.combinations(days_left, number_of_more_days_off):
            subset = list(subset)
            subset.extend([self.name + '-' + day for day in self.predefined_days_off])
            possibilities.append(subset)
        return(possibilities)



class Schedule():
    """docstring for Schedule"""
    def __init__(self, classes, teachers):
        self.teachers = teachers
        self.classes = classes


    def get_shifts(self):
        all_lessons = []
        for cl in self.classes.values():
            for lesson_time in cl.lesson_times:
                all_lessons.append(lesson_time)
        shifts = set(all_lessons)
        return shifts


    def create_off_combinations(self):
        group = []
        for teacher in self.teachers.values():
            days_off_possibilities = teacher.get_days_off_possibilities()
            if days_off_possibilities!=[]:
                group.append(days_off_possibilities)
        off_combinations  = itertools.product(*group)
        off_combinations = list(off_combinations)
        return off_combinations

    def find_main_teacher(self, cl):
        for teacher in self.teachers:
            if cl.cl:
                pass


    def put_schedule(self, off_combination):
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        class_teacher_allocations = {shift: [] for shift in self.get_shifts()}
        # reset all lesson numbers to calculate a new schedule:
        for cl in self.classes.values():
            cl.reset_lesson_numbers()

        # process each day of week
        for day in weekdays:
            # get available teacher
            available_teachers = [teacher for teacher in self.teachers.values() 
                                  if not any(teacher.name+'-'+day in sl for sl in off_combination)]

            # get shift then filter shift on the processing day
            shifts = list(filter(lambda shift: day in shift, self.get_shifts()))

            class_list = {shift: [] for shift in shifts}
            teacher_list = {shift: [] for shift in shifts}

            # create class list and teacher list for a shift in the proccessing day
            for shift in shifts:
                class_list[shift] = [cl for cl in self.classes.values()
                                     if shift in cl.lesson_times]
                teacher_list[shift] = available_teachers

            #ALLOCATIONS:
            for shift in shifts:
                if len(teacher_list[shift]) < len(class_list[shift]):
                    return False #'not enough teachers for this case'

                # sort the class_list based on native percentage
                temp_list_to_reorder_classes = [cl.get_native_need_rate() for cl in class_list[shift]]
                class_list[shift] = [cl for temp,cl in sorted(zip(temp_list_to_reorder_classes, class_list[shift]), key=lambda pair: pair[0])]

                # allocate native teachers to their classes: regular or smartchoice based of the need of native rate
                for cl in class_list[shift]:
                    if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place native teacher to their main classes if possible, if not => next
                        if cl in teacher.main_classes and teacher.type=='ntfulltime':
                            if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher in SC classes
                                temp = cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_native_lesson_number()
                                cl.increase_learned_lesson_number()
                                break

                    if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if this teacher done
                        # place native teacher to any in-need class
                        if teacher.type in ['ntfulltime','ntparttime']:
                            if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher 
                                temp = cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_native_lesson_number()
                                cl.increase_learned_lesson_number()
                                break

                    # after this allocation, native teachers might not be allocated to any classes because the need rate is high
                    # need to allocate these teachers later


                # allocate full time and part time vietnamese teachers to their classes: regular based of the need of vn rate
                for cl in class_list[shift]:
                    if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place full time vietnamese teacher to their main classes
                        if cl in teacher.main_classes and teacher.type=='vnfulltime':
                            temp = cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_main_vn_teacher_lesson_number()
                            cl.increase_learned_lesson_number()
                            break

                    
                        if cl in teacher.main_classes and teacher.type=='vnparttime':
                            if cl.get_main_vn_teacher_need_rate() < 66.7: #100*2/3 calcuate the percentage of vn partime main teacher in regular classes
                                temp = cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_main_vn_teacher_lesson_number()
                                cl.increase_learned_lesson_number()
                                break
                
                # allocate full time native teachers to their classes, dont care about any rate
                for cl in class_list[shift]:
                    if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place native teacher to their main classes if possible, if not => next
                        if cl in teacher.main_classes and teacher.type == 'ntfulltime':
                            temp = cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_native_lesson_number()
                            cl.increase_learned_lesson_number()
                            break
            


                # allocate full time teachers left to classes
                remaining_fulltime_teachers = []
                for teacher in teacher_list[shift]:
                    if not any(teacher.name in string for string in class_teacher_allocations[shift]): # check if teacher done
                        if teacher.type=='vnfulltime':
                            remaining_fulltime_teachers.append(teacher)
     
                remaining_teachers = []
                for teacher in teacher_list[shift]:
                    if not any(teacher.name in string for string in class_teacher_allocations[shift]): # check if teacher done
                        remaining_teachers.append(teacher)

                remaining_classes = []
                for cl in class_list[shift]:
                    if not any(cl.class_code in string for string in class_teacher_allocations[shift]): # check if this class done
                        remaining_classes.append(cl)


                if len(remaining_fulltime_teachers) == len(remaining_classes):
                    for cl, teacher in zip(remaining_classes, remaining_fulltime_teachers):
                        temp = 'case enough full time teachers : ' + cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_learned_lesson_number()

                elif len(remaining_fulltime_teachers) > len(remaining_classes):
                    combinations  = itertools.combinations(remaining_fulltime_teachers, len(remaining_classes))
                    combinations = list(combinations)
                    i = 0
                    for combo in combinations:
                        i+=1
                        for cl, teacher  in zip(remaining_classes, combo):
                            temp = 'case redundant fulltime teachers {} : '.format(i) + cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            if i==1: # avoid increasing many times
                                cl.increase_learned_lesson_number()
                        break # take 1 example

                elif len(remaining_fulltime_teachers) < len(remaining_classes):
                    number_of_cases = 0
                    for cl in remaining_classes:
                        for teacher in remaining_teachers:
                            if cl in teacher.main_classes:
                                temp = 'case lack of fulltime teachers : ' + cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_main_vn_teacher_lesson_number()
                                cl.increase_learned_lesson_number()
                                number_of_cases+=1
                                break
                        if number_of_cases==len(remaining_classes) - len(remaining_fulltime_teachers):
                            break

                    # allocate full time teachers to remaining classes
                    for cl in class_list[shift]:
                        if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                        for teacher in teacher_list[shift]:
                            if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                            if teacher.type == 'vnfulltime':
                                temp = 'case lack of fulltime teachers : '  + cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_learned_lesson_number()
                                break

                    # allocate remaining classes
                    for cl in class_list[shift]:
                        if any(cl.class_code in string for string in class_teacher_allocations[shift]): continue # check if this class done
                        for teacher in teacher_list[shift]:
                            if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                            temp = 'case lack of fulltime teachers: '  + cl.class_code  + ' - ' + teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_learned_lesson_number()
                            break


                # teachers and classes left after apply filters above
                for teacher in teacher_list[shift]:
                    if not any(teacher.name in string for string in class_teacher_allocations[shift]): # check if teacher done
                        class_teacher_allocations[shift].append('redundant teacher: ' + teacher.name)
                for cl in class_list[shift]:
                    if not any(cl.class_code in string for string in class_teacher_allocations[shift]): # check if this class done
                        temp = 'unprocessed class: ' + cl.class_code  + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)

        return class_teacher_allocations


    def calculate_assessments(self, schedule):
        # get list of strings of teacher + main class, native teachers:
        main_teachers_classes_list = []
        native_teachers_classes_list = []
        parttime_teachers_classes_list = []
        fulltiem_teachers_classes_list = []
        for teacher in self.teachers.values():
            for cl in teacher.main_classes:
                main_teachers_classes_list.append(cl.class_code +' - '+ teacher.name)
            if teacher.type in ['ntfulltime', 'ntparttime']:
                native_teachers_classes_list.append(teacher.name)
            if teacher.type=='vnparttime':
                parttime_teachers_classes_list.append(teacher.name)
            if teacher.type=='vnfulltime':
                fulltiem_teachers_classes_list.append(teacher.name)
            
        # filter unwanted string in schedule flat list
        schedule_flat_list = [item for sublist in schedule.values() for item in sublist]
        schedule_flat_list = filter(lambda x: 'redundant teacher' not in x and 'unprocessed class' not in x, schedule_flat_list) 
        schedule_flat_list = list(schedule_flat_list)
        #==============
        # TỈ LỆ ĐÚNG LỚP
        # count the occurences main_teachers_classes_list in schedule
        right_teacher_count = 0
        for each_string in main_teachers_classes_list:
            right_teacher_count += sum(each_string in s for s in schedule_flat_list)

        #==============
        # TỈ LỆ GIÁO VIÊN NƯỚC NGOÀI
        native_teacher_count = 0
        for each_string in native_teachers_classes_list:
            native_teacher_count += sum(each_string in s for s in schedule_flat_list)


        #==============
        # TỈ LỆ SỬ DỤNG GV PART TIME
        parttime_teacher_count = 0
        for each_string in parttime_teachers_classes_list:
            parttime_teacher_count += sum(each_string in s for s in schedule_flat_list)


        #==============
        # TỈ LỆ CÂN BẰNG GIÁO VIÊN FULL TIME VIỆT NAM
        print('number of lessons for each vn fulltime teacher:')
        for each_string in fulltiem_teachers_classes_list:
            self.teachers[each_string].lesson_count = sum(each_string in s for s in schedule_flat_list)
            print(each_string, self.teachers[each_string].lesson_count)


        print('number of lessons having main teachers: {}/{} lessons'.format(right_teacher_count,len(schedule_flat_list)))
        print('number of lessons having native teachers: {}/{} lessons'.format(native_teacher_count,len(schedule_flat_list)))
        print('number of lessons using vn parttime teachers: {}/{} lessons'.format(parttime_teacher_count,len(schedule_flat_list)))

        #tỉ lê gv nước ngoài
        # tỉ lệ full time
        # tỉ lệ xài giáo viên parttime
        # tỉ lệ cân bằng giáo viên full time
        





    def print_schedule(self, schedule):
        self.calculate_assessments(schedule)
        shifts = ['mon-17h40-19h10',
                  'mon-19h20-20h50',
                  'tue-17h40-19h10',
                  'tue-19h20-20h50',
                  'wed-17h40-19h10',
                  'wed-19h20-20h50',
                  'thu-17h40-19h10',
                  'thu-19h20-20h50',
                  'fri-17h40-19h10',
                  'fri-19h20-20h50',
                  'sat-08h00-09h30',
                  'sat-09h50-11h20',
                  'sat-17h40-19h10',
                  'sat-19h20-20h50',
                  'sun-08h00-09h30',
                  'sun-09h50-11h20']
        for shift in shifts:
            for each in schedule[shift]:
                #print(shift, each)
                pass
            #print('\n')
            pass
        print('\n')

    def find_best_schedule(self):
        i=0
        s = time.time()
        off_combinations = self.create_off_combinations()
        for off_combination in off_combinations:
            s = time.time()
            print(off_combination)
            result_schedule = self.put_schedule(off_combination)
            if result_schedule!=False:
                self.print_schedule(result_schedule)
                i+=1
                print(i, len(off_combinations))
                if i==1: break
            
            print(time.time()-s)







#==================================================

teachers = {}
teacher_names = list(set([x[1] for x in data]))
for teacher_name in teacher_names:
    if teacher_name!='NoTeacher':
        teachers[teacher_name] = Teacher(teacher_name)

teachers['Ms.Mia'].predefined_days_off = ['mon']
teachers['Ms.Phúc'].type = 'vnparttime'
teachers['Mr.Noland'].type = 'vnparttime'
teachers['Ms.Jenni'].type = 'vnparttime'

teachers['Mr.Andre'].type = 'ntfulltime'
teachers['Mr.Matt'].type = 'ntfulltime'

teachers['Mr.Andre'].number_of_off_days = 2
teachers['Mr.Matt'].number_of_off_days = 2

teachers['Mr.Kay'].improper_classes = ['SCA2A2-101020']


# to do: check imporper class are not main classes

classes = {}
for each_row in data:
    lesson_times = each_row[2]
    class_code = each_row[0]
    teacher_name = each_row[1]
    native_lesson_number = each_row[3]
    main_vn_teacher_lesson_number = each_row[4]
    classes[class_code] = InsClass(class_code, lesson_times, native_lesson_number, main_vn_teacher_lesson_number)
    if teacher_name!='NoTeacher':
       teachers[teacher_name].main_classes.append(classes[class_code])


schedule = Schedule(classes,teachers)
schedule.find_best_schedule()



# note thời gian partime vaof lớp là 70%, native là 20%, other teacher là 10% ???