



from input_excel import Data
from models import Teacher, InsClass
from models import get_class_by_name, get_teacher_by_name
from schedule import Schedule

data = Data()
teachers = []
for index, row in data.teachers.iterrows():
    teacher = Teacher(
            row['name'],
            row['type'],
            row['predefined_days_off'],
            row['number_days_off'],
            row['improper_class_names'])
    teachers.append(teacher)

classes = []
for index, row in data.classes.iterrows():
    cl = InsClass(
            row['class_name'],
            get_teacher_by_name(row['teacher_name']),
            row['time_frames'],
            row['native_lesson_count'],
            row['main_vn_teacher_lesson_count'])
    classes.append(cl)



import time

schedule = Schedule(classes, teachers)
s = time.time()
schedule.find_best_schedule()
print(time.time()-s)
'''
schedule.find_best_schedule_for_day('tue')
schedule.find_best_schedule_for_day('wed')
schedule.find_best_schedule_for_day('thu')
schedule.find_best_schedule_for_day('fri')
schedule.find_best_schedule_for_day('sat')
schedule.find_best_schedule_for_day('sun')
'''
#schedule.class_native_rate()
#print(number)





# note thời gian partime vaof lớp là 70%, native là 20%, other teacher là 10% ???
# todo: không nên xét trường hợp giáo viên làm 3 ca 1 ngày, nếu không đủ mới xét 4 ca 1 ngày