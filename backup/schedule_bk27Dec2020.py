from datetime import date
import math

import sys


import itertools

data = [['SK1B1-121220', 'Ms.Mia', ['sat-08h00-09h30', 'sun-08h00-09h30']],
['SK1P1-031020', 'Ms.Jay', ['sat-08h00-09h30', 'sun-08h00-09h30']],
['SK1A2-101020', 'Ms.Amy', ['sat-08h00-09h30', 'sun-08h00-09h30']],
['SCA2A2-101020', 'NoTeacher', ['sat-09h50-11h20', 'sun-09h50-11h20']],
['SK2B3-241020', 'Ms.Jay', ['sat-09h50-11h20', 'sun-09h50-11h20']],
['SK2M2-171020', 'Mr.Noland', ['sat-09h50-11h20', 'sun-09h50-11h20']],
['SK3B4-111020', 'Ms.Mia', ['sat-09h50-11h20', 'sun-09h50-11h20']],
['ST3B3-261020', 'Ms.Amy', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['ST3D2-041220', 'Ms.Jay', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['ST4C2-021220', 'Mr.Windy', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['ST2G2-231120', 'Ms.Phúc', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['SB3E1-131120', 'Mr.Noland', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['SK2K3-300920', 'Ms.Misty', '', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10']],
['SK1O2-191020', 'Ms.Jenni', ['mon-17h40-19h10', 'wed-17h40-19h10']],
['SCB3C2-251120', 'NoTeacher', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['SL2G3-280920', 'Ms.Jay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['ST2H1-161120', 'Ms.Mia', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['SL3F1-111120', 'Mr.Windy', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['SL1A2-071220', 'Ms.Jenni', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['IE3A1-251120', 'Mr.Kay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50']],
['SK2N1-071120', 'Mr.Windy', ['wed-17h40-19h10', 'sat-17h40-19h10']],
['SCB2A1-081020', 'NoTeacher', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['SK3E1-271020', 'Ms.Jay', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['SK2H4-031120', 'Ms.Misty', '', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['SB4C1-191120', 'Ms.Amy', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['ST1E2-211120', 'Mr.Kay', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['ST2F3-260920', 'Ms.Mia', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10']],
['SCB3B3-081220', 'NoTeacher', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50']],
['SL3B4-101120', 'Ms.Jenni', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50']],
['ST1A2-311020', 'Ms.Amy', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50']]]





class InsClass():
    """docstring for InsClass"""
    def __init__(self, class_code, lesson_times):
        self.class_code = class_code
        self.start_date = self.class_code[-6:]
        self.lesson_times = lesson_times
        self.week_num = self.get_week_num()

    def get_week_num(self):
        # get year month day from classcode
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
    def __init__(self, name, full_time=True, 
            main_classes=None, 
            pre_defined_off_days=None,
            improper_classes=None):
        self.name = name
        if main_classes==None:
            self.main_classes = []
        else:
            self.main_classes = main_classes

        if improper_classes==None:
            self.improper_classes = []
        else:
            self.improper_classes = improper_classes

        if pre_defined_off_days==None:
            self.pre_defined_off_days = []
        else:
            self.pre_defined_off_days = pre_defined_off_days

        self.full_time = full_time
        


    def get_work_schedule(self):
        schedule = []
        for cl in self.main_classes:
            for lesson_time in cl.lesson_times:
                for off_day in self.off_days:
                    if off_day in lesson_time:
                        break
                schedule.append(cl.class_code + ' --- ' +lesson_time)
        return schedule


    def get_session_number(self):
        num = 0
        for cl in self.main_classes:
            num += len(cl.lesson_times)
        return num
 


class Schedule():
    """docstring for Schedule"""
    def __init__(self, classes, teachers):
        self.teachers = teachers
        self.classes = classes

    def get_all_lessons(self):
        all_lessons = []
        for cl in self.classes.values():
            for lesson_time in cl.lesson_times:
                all_lessons.append(lesson_time)
        return all_lessons

    def get_shifts(self):
        all_lessons = self.get_all_lessons()
        shifts = set(all_lessons)
        return shifts


    def get_number_of_lessons_in_shift(self):
        weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
        all_lessons = self.get_all_lessons()
        shifts = set(all_lessons)
        lesson_number_in_shifts = {shift: all_lessons.count(shift) for shift in shifts}
        return lesson_number_in_shifts

    def get_available_number_of_teachers_in_shift(self, typ='all'): #all, fulltime, parttime
        shifts = self.get_shifts()
        teacher_number_in_shifts = {shift: 0 for shift in shifts}

        for shift in shifts:
            for teacher in self.teachers.values():
                if typ=='fulltime':
                    if not teacher.full_time:
                        continue

                if typ=='parttime':
                    if teacher.full_time:
                        continue

                off_flag = False
                for day in teacher.pre_defined_off_days:
                    if day in shift:
                        off_flag = True
                        break

                if not off_flag:
                    teacher_number_in_shifts[shift] += 1
        return teacher_number_in_shifts




    def create_perfect_schedule(self):
        shifts = self.get_shifts()
        schedule = {shift: [] for shift in shifts}
        for shift in shifts:
            for teacher in self.teachers.values():
                for cl in teacher.main_classes:
                    if shift in cl.lesson_times:
                        schedule[shift].append([cl, teacher])
        return schedule



    def get_available_teachers_if_perfect(self):
        perfect_schedule = self.create_perfect_schedule()
        shifts = self.get_shifts()
        available_teachers = {shift: [] for shift in shifts}
        for shift in shifts:
            perfect_schedule_shift_teachers = [schedule_shift[1] for schedule_shift in perfect_schedule[shift]]
            for teacher in self.teachers.values():
                filter_flag = False
                for each in perfect_schedule[shift]:
                    if each[1]==teacher:
                        filter_flag = True
                        break

                if not filter_flag and teacher.name!='NoTeacher':
                    available_teachers[shift].append(teacher)
        return available_teachers



    def process_each_day(self, day='mon'):
        perfect_schedule = self.create_perfect_schedule()
        available_teachers_if_perfect = self.get_available_teachers_if_perfect()
        shifts = list(filter(lambda shift: day in shift, self.get_shifts()))
        
        print('\n filter day')
        print(shifts)

        class_list = {shift: [] for shift in shifts}
        teacher_list = {shift: [] for shift in shifts}
        for shift in shifts:
            class_list[shift] = [schedule_shift[0] for schedule_shift in perfect_schedule[shift]]
            
        teacher_list = list(self.teachers.values())
        teacher_list = list(filter(lambda teacher: teacher.name!='NoTeacher' and day not in teacher.pre_defined_off_days, teacher_list))
        teacher_list = [teacher.name for teacher in teacher_list]


        print(teacher_list)
        max_number_classes_shift = max([len(cl) for  cl in class_list.values()])
        max_number_teacher_shift = len(teacher_list)
        number_teachers_can_be_off = max_number_teacher_shift - max_number_classes_shift

        # list all possibilities for off teachers
        print('\n off list')
        for subset in itertools.combinations(teacher_list, number_teachers_can_be_off):
            print(subset)



    def process_each_day_reserve(self, day='mon'):
        perfect_schedule = self.create_perfect_schedule()
        available_teachers_if_perfect = self.get_available_teachers_if_perfect()
        shifts = list(filter(lambda shift: day in shift, self.get_shifts()))
        
        print('\n filter day')
        print(shifts)

        '''
        for shift in shifts:
            for cl, teacher in perfect_schedule[shift]:
                if teacher.name=='NoTeacher' \
                        or day in teacher.pre_defined_off_days:
                    
                    print(teacher.name)
                    #for available_teachers in available_teachers_if_perfect:
                        
        '''


teachers = {}
teacher_names = list(set([x[1] for x in data]))
for teacher_name in teacher_names:
    teachers[teacher_name] = Teacher(teacher_name)

teachers['Ms.Mia'].pre_defined_off_days = ['mon', 'sat']
teachers['Ms.Phúc'].full_time = False
teachers['Mr.Noland'].full_time = False
teachers['Ms.Jenni'].full_time = False
teachers['Ms.Misty'].full_time = False
teachers['Mr.Kay'].improper_classes = ['SCA2A2-101020']



classes = {}
for each_row in data:
    lesson_times = each_row[2]
    class_code = each_row[0]
    teacher_name = each_row[1]
    classes[class_code] = InsClass(class_code, lesson_times)

    teachers[teacher_name].main_classes.append(classes[class_code])


schedule = Schedule(classes,teachers)
print(schedule.get_number_of_lessons_in_shift())
print()
print(schedule.get_available_number_of_teachers_in_shift(typ='all'))
print()
print(schedule.get_available_number_of_teachers_in_shift(typ='fulltime'))
print()
print(schedule.get_available_number_of_teachers_in_shift(typ='parttime'))

print('\n\ncreate_perfect_schedule')
perfect_schedule = schedule.create_perfect_schedule()

for shift, info in perfect_schedule.items():
    if 'mon' in shift:
        print(shift, [[x[0].class_code, x[1].name] for x in info])


print('\n\nget_available_teachers_if_perfect')
available_teachers = schedule.get_available_teachers_if_perfect()

for shift, teachers in available_teachers.items():
    if 'mon' in shift:
        print(shift, [x.name for x in teachers])



schedule.process_each_day(day='mon')
# 1. lấy perfect schedule (xếp đúng gv, chưa có lịch nghỉ)
# 2. lấy danh sách giáo viên rảnh theo perfect schedule
# 3. xét từng ngày,
# 3.1. bỏ 'noteacher' => đủ gv không, kiểm tra level của gv phù hợp lớp không => Nếu đủ đến bước tiếp theo, Nếu không đủ báo động
# 3.2. bỏ các ngày gv xin nghỉ phép ra => đủ gv không, kiểm tra level gv phù hợp không
# => không đủ => báo động => không cho nghỉ
# => vừa đủ => không cho gv nào khác nghỉ ngày này => xuất schedule ngày này
# => dư => lưu tất cả các khả năng có thể cho gv nghỉ trong từng ngày
# 4. dựa vào khả năng cho gv nghỉ trong tuần ở bước 3 => chạy ra tất cả kế hoạch sắp xếp gv nghỉ => ở mỗi kế hoạch, tính số liệu về số buổi gvnn/tổng số buổi trong khóa, gvpartime/.., gvfulltime/.. => tìm bộ số tối ưu
# 5. lấy lịch xếp có bộ số tối ưu nhất => xuất
