






import pandas as pd
from pathlib import Path


import re

filenames = ['Chương trình học lớp PCH-SK1B1-121220.xlsx',
'Chương trình học lớp PCH-ST2F4-171220.xlsx',
'Chương trình học lớp PCH-IE3A1-251120.xlsx',
'Chương trình học lớp PCH-SK4B1-020121.xlsx',
'Chương trình học lớp PCH-SK1O3-060121.xlsx',
'Chương trình học lớp PCH-ST2G2-231120.xlsx',
'Chương trình học lớp PCH-SB3E1-131120.xlsx',
'Chương trình học lớp PCH-SL1A2-071220.xlsx',
'Chương trình học lớp PCH-SK1P2-201220.xlsx',
'Chương trình học lớp PCH-ST2H1-161120.xlsx',
'Chương trình học lớp PCH-SB4C1-191120.xlsx',
'Chương trình học lớp PCH-SL2G4-181220.xlsx',
'Chương trình học lớp PCH-SK2B4-100121.xlsx',
'Chương trình học lớp PCH-ST3B4-180121.xlsx',
'Chương trình học lớp PCH-SCA2A3-271220.xlsx',
'Chương trình học lớp PCH-SL3B4-101120.xlsx',
'Chương trình học lớp PCH-SK2K4-211220.xlsx',
'Chương trình học lớp PCH-ST3D2-041220.xlsx',
'Chương trình học lớp PCH-SCB2A2-291220.xlsx',
'Chương trình học lớp PCH-SL3F1-111120.xlsx',
'Chương trình học lớp PCH-SK2M3-030121.xlsx',
'Chương trình học lớp PCH-ST4C2-021220.xlsx',
'Chương trình học lớp PCH-SCB3B3-081220.xlsx',
'Chương trình học lớp PCH-ST1A3-210121.xlsx',
'Chương trình học lớp PCH-SK2N1-071120.xlsx',
'Chương trình học lớp PCH-SK1A3-271220.xlsx',
'Chương trình học lớp PCH-ST1E2-211120.xlsx',
'Chương trình học lớp PCH-SK3E2-160121.xlsx']

class Excel:
    # Contructor
    def __init__(self, path, sheet_names):
        self.sheets = self.load_dtb(path, sheet_names) # a dict to contain all sheets data frame
    # load dtb from excel or pickle files
    @staticmethod
    def load_dtb_reserved(path, sheet_names):
        # create data frames from pickle files if not create pickle files
        sheets = {}
        for sheet_name in sheet_names:
            print('read excel files: ', path)
            sheets[sheet_name] = pd.read_excel(path, 
                                               sheet_name=sheet_name, 
                                               header=0, 
                                               na_values='#### not defined ###', 
                                               keep_default_na=False)
        return sheets
    @staticmethod
    def load_dtb(path, sheet_names):
        # create data frames from pickle files if not create pickle files
        sheets = {}
        filename = Path(path).stem # get file name of ymme path
        
        for sheet_name in sheet_names:
            # print('Processing ' + filename + '_sheet_' + sheet_name)
            # read pickle data
            try: 
                pickled_fpath = str(path).replace('.xlsx','') + '_sheet_' + sheet_name
                print('read picked files: ', pickled_fpath)
                sheets[sheet_name] = pd.read_pickle(pickled_fpath)
            
            # if failed to read => read excel file and write pickle
            except FileNotFoundError as e:
                print('read excel files: ', path)
                sheets[sheet_name] = pd.read_excel(path, 
                                                   sheet_name=sheet_name, 
                                                   header=0, 
                                                   na_values='#### not defined ###', 
                                                   keep_default_na=False)

                pickled_fpath = str(path).replace('.xlsx','') + '_sheet_' + sheet_name
                print('write picked files', pickled_fpath)
                sheets[sheet_name].to_pickle(pickled_fpath)
        return sheets



sheets = ['program']

for path in filenames:
	excel_path = 'Classes/' + path
	df = Excel(excel_path, sheets).sheets['program']
	df = df['Buổi học']
	l = df.tolist()
	l = list(filter(lambda x: '-' in x and '/' not in x, l))
	s = set(l)

	print(excel_path)
	for each in s:
		print(each, ' :', l.count(each))
	print('\n\n')

import sys
sys.exit()














each_string = 'foo'
schedule = ["the foo is all fooed", "the bar is all barred", "foo is now a bar"]
count = sum(each_string in s for s in schedule)
print(count)

import sys
sys.exit()




import itertools
list1 = ['gv1','gv2','gv3']
list2 = ['x','y']

group =[list1,list2]
combinations  = itertools.combinations(list1, len(list2))
combinations = list(combinations)


dic = {'a':'1', 'b':'2'}

print(list(zip([1,2],[3,4])))
import sys
sys.exit()
'''


data = [['SK1B1-121220', 'Ms.Mia', ['sat-08h00-09h30', 'sun-08h00-09h30'], 4, 1['SK1P2-201220', 'Ms.Jay', ['sat-08h00-09h30', 'sun-08h00-09h30'], 1, 29],
['SK1A3-271220', 'Ms.Amy', ['sat-08h00-09h30', 'sun-08h00-09h30'], 1, 22],
['SCA2A3-271220', 'Mr.Andre', ['sat-09h50-11h20', 'sun-09h50-11h20'], 4, 14],
['SK2B3-241020', 'Ms.Jay', ['sat-09h50-11h20', 'sun-09h50-11h20'], 4, 18],
['SK2M3-030121', 'Mr.Noland', ['sat-09h50-11h20', 'sun-09h50-11h20'], 3, 14],
['SK4B1-020121', 'Ms.Mia', ['sat-09h50-11h20', 'sun-09h50-11h20'], 5, 11],
['ST3B3-261020', 'Ms.Amy', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 4, 27],
['ST3D2-041220', 'Ms.Jay', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 2, 14],
['ST4C2-021220', 'Mr.Kay', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 3, 17],
['ST2G2-231120', 'Ms.Phúc', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 3, 22],
['SB3E1-131120', 'Mr.Noland', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 5, 12],
['SK2K4-211220', 'Ms.Misty', ['mon-17h40-19h10', 'wed-17h40-19h10', 'fri-17h40-19h10'], 3, 24],
['SK1O2-191020', 'Ms.Jenni', ['mon-17h40-19h10', 'wed-17h40-19h10'], 3, 29],
['SCB3C2-251120', 'Mr.Andre', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 5, 12],
['SL2G4-181220', 'Ms.Jay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 5, 13],
['ST2H1-161120', 'Ms.Mia', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 4, 17],
['SL3F1-111120', 'Mr.Windy', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 3, 28],
['SL1A2-071220', 'Ms.Jenni', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 5, 24],
['IE3A1-251120', 'Mr.Kay', ['mon-19h20-20h50', 'wed-19h20-20h50', 'fri-19h20-20h50'], 2, 12],
['SK2N1-071120', 'Mr.Windy', ['wed-17h40-19h10', 'sat-17h40-19h10'], 4, 12],
['SCB2A2-291220', 'Mr.Matt', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 1, 22],
['SK3E1-271020', 'Ms.Jay', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 2, 29],
['SB4C1-191120', 'Ms.Amy', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 1, 25],
['ST1E2-211120', 'Mr.Kay', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 3, 20],
['ST2F4-171220', 'Ms.Mia', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 2, 28],
['SCB3B3-081220', 'Mr.Matt', ['tue-17h40-19h10', 'thu-17h40-19h10', 'sat-17h40-19h10'], 4, 14],
['SL3B4-101120', 'Ms.Jenni', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 1, 23],
['SL1C1-050121', 'Ms.Mia', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 1, 16],
['ST1A2-311020', 'Ms.Amy', ['tue-19h20-20h50', 'thu-19h20-20h50', 'sat-19h20-20h50'], 2, 22]]

teachers['Ms.Mia'].predefined_days_off = ['mon']
teachers['Ms.Phúc'].type = 'vnparttime'
teachers['Mr.Noland'].type = 'vnparttime'
teachers['Ms.Jenni'].type = 'vnparttime'
teachers['Ms.Misty'].type = 'vnparttime'

teachers['Mr.Andre'].type = 'ntfulltime'
teachers['Mr.Matt'].type = 'ntfulltime'

teachers['Mr.Andre'].number_of_off_days = 2
teachers['Mr.Matt'].number_of_off_days = 2

teachers['Mr.Kay'].improper_classes = ['SCA2A2-101020']



print(len(None))

import itertools
A = [[1],[2],[3]]
B = [['a'],['b'],['c']]
C = [['x'],['y'],['z']]
group =[A,B,C]
result  = itertools.product(*group)
for subset in result:
	print(subset)


    def create_perfect_schedule(self):
        shifts = self.get_shifts()
        schedule = {shift: [] for shift in shifts}
        for shift in shifts:
            for teacher in self.teachers.values():
                for cl in teacher.main_classes:
                    if shift in cl.lesson_times:
                        schedule[shift].append([cl, teacher])
        return schedule




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
        teacher_list = list(filter(lambda teacher: teacher.name!='NoTeacher' and day not in teacher.predefined_days_off, teacher_list))
        teacher_list = [teacher.name for teacher in teacher_list]


        print(teacher_list)
        max_number_classes_shift = max([len(cl) for  cl in class_list.values()])
        max_number_teacher_shift = len(teacher_list)
        number_teachers_can_be_off = max_number_teacher_shift - max_number_classes_shift

        # list all possibilities for off teachers
        print('\n off list')
        for subset in itertools.combinations(teacher_list, number_teachers_can_be_off):
            print(subset)

        print()





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

'''