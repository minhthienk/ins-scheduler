import itertools
import sys
import time
import random

from models import get_teacher_by_name, get_class_by_name, get_teacher_main_classes

class Schedule():
    """docstring for Schedule"""
    WEEKDAYS = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
    def __init__(self, classes, teachers):
        self.teachers = teachers
        self.classes = classes
        self.shifts = self.get_shifts()

    def get_shifts(self):
        all_lessons = []
        for cl in self.classes:
            for lesson_time in cl.time_frames:
                all_lessons.append(lesson_time)
        shifts = set(all_lessons)
        return shifts

    def class_native_rate(self):
        # tiêu chí chọn ngày nghỉ gvnn:
        # 1. lớp thiếu nhiều buổi
        # 2. ngày nhiều lớp
        for cl in self.classes:
            print(cl.class_name, cl.get_native_need_rate())

    # note: ý tưởng chọn ngày nghỉ:
    # chạy từng ngày, xét thông số các ngày đó, xem thử cho giáo viên nào nghỉ thì thông số nhỏ nhất

    def refine_days_off_possibilities(self):
        number_teachers = len(self.teachers)
        
        for shift in self.shifts:
            number_classes = len([cl for cl in self.classes if shift in cl.time_frames]) 
            if number_teachers < number_classes:
                print('there is not enough teacher in the shift:', shift)
            elif number_teachers >= number_classes:
                print(shift, number_teachers - number_classes)


    def create_off_combinations(self):
        groups = []
        number_of_combinations = 1
        for teacher in self.teachers:
            days_off_possibilities = teacher.get_days_off_possibilities()
            length = len(days_off_possibilities)
            number_of_combinations = number_of_combinations*length if length!=0 else number_of_combinations
            if days_off_possibilities!=[]:
                groups.append(days_off_possibilities)
        off_combinations  = itertools.product(*groups)
        return number_of_combinations, off_combinations


    def create_off_combinations_a_day(self, day):
        groups = []
        off_possibilities = []

        max_number_classes = 0
        for shift in self.shifts:
            if day in shift:
                number_classes = len([cl for cl in self.classes if shift in cl.time_frames]) 
                if number_classes > max_number_classes:
                    max_number_classes = number_classes

        for teacher in self.teachers:
            days_off_possibilities = teacher.get_days_off_possibilities()
            for possibility in days_off_possibilities:
                if any(day in string for string in possibility):
                    off_possibilities.append(teacher.name)

        off_possibilities = set(off_possibilities)
        off_combinations = []
        for r in range(1,len(self.teachers)-max_number_classes+1):
            off_combinations.extend(itertools.combinations(off_possibilities, r))

        return off_combinations



    def get_least_busy_teacher(self, teachers, considered_type):
        ''' get the leaste busy teacher of each type'''
        min_number = 999
        selected = None
        for teacher in teachers:
            # prevent the case when parttime teaches when asup is still free
            if considered_type== 'vnparttime' and teacher.type=='asup':
                return teacher

            if teacher.type == considered_type or teacher.type=='asup':
                # asup will be the last one doing backup
                if teacher.type=='asup':
                    if len(teachers)==1:
                        return teacher
                    else:
                        continue
                # find the teacher having the least lesson count
                if teacher.lesson_count<min_number:
                    min_number = teacher.lesson_count
                    selected = teacher
        if selected!=None:
            return selected
        else:
            return None





    def find_best_schedule_for_day(self,day):
        i=0
        off_combinations = self.create_off_combinations_a_day(day)
        schedules = {}
        for off_combination in off_combinations:
            #print(off_combination)
            schedule = self.put_schedule_day(off_combination, day)
            schedules[off_combination] = self.put_schedule_day(off_combination, day)
            #self.print_schedule(schedule)
            #print(self.calculate_assessments(schedule)['native usage'])
        print(len(schedules))


        print('filter unprocessed class')
        temp_schedules = {}
        #print(max_val)
        for off_combination in schedules.keys():
            if self.calculate_assessments(schedules[off_combination])['is not done']  == False:
                temp_schedules[off_combination] = schedules[off_combination]
        schedules = temp_schedules
        temp_schedules = {}
        print(len(schedules))

        print('filter max native usage')
        temp_schedules = {}
        max_val = max([self.calculate_assessments(schedule)['native usage'] for schedule in schedules.values()])
        #print(max_val)
        for off_combination in schedules.keys():
            if self.calculate_assessments(schedules[off_combination])['native usage']  == max_val:
                temp_schedules[off_combination] = schedules[off_combination]
        schedules = temp_schedules
        temp_schedules = {}
        print(len(schedules))


        print('filter max main teacher usage')
        temp_schedules = {}
        max_val = max([self.calculate_assessments(schedule)['main teacher'] for schedule in schedules.values()])
        #print(max_val)
        for off_combination in schedules.keys():
            if self.calculate_assessments(schedules[off_combination])['main teacher']  == max_val:
                temp_schedules[off_combination] = schedules[off_combination]
        schedules = temp_schedules
        temp_schedules = {}
        print(len(schedules))


 
        print('filter min parttime teacher usage')
        temp_schedules = {}
        min_val = min([self.calculate_assessments(schedule)['parttime usage'] for schedule in schedules.values()])
        #print(min_val)
        for off_combination in schedules.keys():
            if self.calculate_assessments(schedules[off_combination])['parttime usage']  == min_val:
                temp_schedules[off_combination] = schedules[off_combination]
        schedules = temp_schedules
        temp_schedules = {}
        print(len(schedules))



        print('filter teacher balance')
        temp_schedules = {}
        min_val = min([self.calculate_assessments(schedule)['teacher work balance'] for schedule in schedules.values()])
        #print(min_val)
        for off_combination in schedules.keys():
            if self.calculate_assessments(schedules[off_combination])['teacher work balance']  == min_val:
                temp_schedules[off_combination] = schedules[off_combination]
        schedules = temp_schedules
        temp_schedules = {}
        print(len(schedules))



        for off_combination, shedule in schedules.items():
            print(off_combination)
            self.print_schedule(shedule)


        '''
        print('number of lessons having main teachers: {}/{} lessons'.format(right_teacher_count,len(schedule_flat_list)))
        print('number of lessons having native teachers: {}/{} lessons'.format(native_teacher_count,len(schedule_flat_list)))
        print('number of lessons using vn parttime teachers: {}/{} lessons'.format(parttime_teacher_count,len(schedule_flat_list)))
        print('teacher lessont count balance rate: {}/{} ({})'.format(min(lesson_counts),max(lesson_counts),min(lesson_counts)/max(lesson_counts)))
        '''




    def put_schedule_day(self, off_combination, day):
        for cl in self.classes:
            cl.reset_lesson_numbers()
        for teacher in self.teachers:
            teacher.lesson_count = 0


        class_teacher_allocations = {shift: [] for shift in self.shifts if day in shift}

        # get available teacher
        available_teachers = [teacher for teacher in self.teachers
                              if not any(teacher.name in element for element in off_combination)]

        # get shift then filter shift on the processing day
        day_shifts = list(filter(lambda shift: day in shift, self.shifts))
        class_list = {shift: [] for shift in day_shifts}
        teacher_list = {shift: [] for shift in day_shifts}

        # create class list and teacher list for a shift in the proccessing day
        for shift in day_shifts:
            class_list[shift] = [cl for cl in self.classes
                                 if shift in cl.time_frames]
            teacher_list[shift] = available_teachers


        #ALLOCATIONS:
        for shift in day_shifts:
            if len(teacher_list[shift]) < len(class_list[shift]):
                return False #'not enough teachers for this case'

            # sort the class_list based on native percentage
            temp_list_to_reorder_classes = [cl.get_native_need_rate() for cl in class_list[shift]]
            class_list[shift] = [cl for temp,cl in sorted(zip(temp_list_to_reorder_classes, class_list[shift]), key=lambda pair: pair[0])]

            # allocate native teachers to their classes: regular or smartchoice based of the need of native rate
            for cl in class_list[shift]:
                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                for teacher in teacher_list[shift]:
                    if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                    # place native teacher to their main classes if possible, if not => next
                    if cl.teacher is teacher and teacher.type=='ntfulltime':
                        if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher in SC classes
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_native_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break

                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                for teacher in teacher_list[shift]:
                    if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if this teacher done
                    # place native teacher to any in-need class
                    if teacher.type in ['ntfulltime','ntparttime']:
                        if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher 
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_native_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break

                # after this allocation, native teachers might not be allocated to any classes because the need rate is high
                # need to allocate these teachers later


            # allocate full time and part time vietnamese teachers to their classes: regular based of the need of vn rate
            for cl in class_list[shift]:
                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                for teacher in teacher_list[shift]:
                    if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                    # place full time vietnamese teacher to their main classes
                    if cl.teacher is teacher and teacher.type=='vnfulltime':
                        temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_main_vn_teacher_lesson_count()
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1
                        break

                
                    if cl.teacher is teacher and teacher.type=='vnparttime':
                        if cl.get_main_vn_teacher_need_rate() < 66.7: #100*2/3 calcuate the percentage of vn partime main teacher in regular classes
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_main_vn_teacher_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break
            
            # allocate full time native teachers to their classes, dont care about any rate
            for cl in class_list[shift]:
                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                for teacher in teacher_list[shift]:
                    if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                    # place native teacher to their main classes if possible, if not => next
                    if cl.teacher is teacher and teacher.type == 'ntfulltime':
                        temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_native_lesson_count()
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1
                        break
        

            #==============================================
            # allocate teachers left to classes
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
                if not any(cl.class_name in string for string in class_teacher_allocations[shift]): # check if this class done
                    remaining_classes.append(cl)


            # get list of classes which have main teacher as parttime
            temp_classes_for_part_time_teachers = []
            temp_parttime_teachers_allocation = []
            for cl in remaining_classes:
                for teacher in remaining_teachers:
                    if cl.teacher is teacher:
                        temp_classes_for_part_time_teachers.append(cl)
                        temp_parttime_teachers_allocation.append(teacher)
                        break


            # arrange remaining full time teachers to remaining classes which dont have main teacher 
            for cl in remaining_classes:
                if cl not in temp_classes_for_part_time_teachers:
                    proper_teachers = []
                    for teacher in remaining_teachers:
                        if cl.class_name not in teacher.improper_class_names and teacher not in temp_parttime_teachers_allocation:
                            if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                                proper_teachers.append(teacher)
                
                    least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnfulltime')
                    if least_busy_teacher!=None:
                        temp = 'arrange remaining full time teachers to remaining classes which dont have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1



            # arrange remaining part time teachers remaining classes which dont have main teacher 
            for cl in remaining_classes:
                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                if cl not in temp_classes_for_part_time_teachers:
                    proper_teachers = []
                    for teacher in remaining_teachers:
                        if cl.class_name not in teacher.improper_class_names and teacher not in temp_parttime_teachers_allocation:
                            if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                                proper_teachers.append(teacher)

                    least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnparttime')
                    if least_busy_teacher!=None:

                        temp = 'arrange remaining part time teachers remaining classes which dont have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1

            # TODO: 


            # arrange remaining full time teachers to partime classes which have main teacher 
            # todo: get check which class is proper to take back (random or priority)
            for cl in temp_classes_for_part_time_teachers:
                proper_teachers = []
                for teacher in remaining_teachers:
                    if cl.class_name not in teacher.improper_class_names:
                        if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                            proper_teachers.append(teacher)
                
                least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnfulltime')
                if least_busy_teacher!=None:
                    temp = 'arrange remaining full time teachers to partime classes which have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                    class_teacher_allocations[shift].append(temp)
                    cl.increase_learned_lesson_number()
                    teacher.lesson_count += 1


            # allocate part time vietnamese teachers to their classes remaining:
            for cl in class_list[shift]:
                if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                for teacher in teacher_list[shift]:
                    if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                    # place full time vietnamese teacher to their main classes
                    if cl.teacher is teacher:
                        temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_main_vn_teacher_lesson_count()
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1
                        break

            # teachers and classes left after apply filters above
            for teacher in teacher_list[shift]:
                if not any(teacher.name in string for string in class_teacher_allocations[shift]): # check if teacher done
                    class_teacher_allocations[shift].append('redundant teacher: ' + teacher.name)
            for cl in class_list[shift]:
                if not any(cl.class_name in string for string in class_teacher_allocations[shift]): # check if this class done
                    temp = 'unprocessed class: ' + cl.class_name  + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                    class_teacher_allocations[shift].append(temp)

        return class_teacher_allocations


    def put_scheduledk(self, off_combination):
        class_teacher_allocations = {shift: [] for shift in self.shifts}
        # reset all lesson numbers to calculate a new schedule:
        for cl in self.classes:
            cl.reset_lesson_numbers()
        for teacher in self.teachers:
            teacher.lesson_count = 0


        # process each day of week
        for day in Schedule.WEEKDAYS:
            # get available teacher
            available_teachers = [teacher for teacher in self.teachers
                                  if not any(teacher.name+'-'+day in sl for sl in off_combination)]

            # get shift then filter shift on the processing day
            day_shifts = list(filter(lambda shift: day in shift, self.shifts))

            class_list = {shift: [] for shift in day_shifts}
            teacher_list = {shift: [] for shift in day_shifts}

            # create class list and teacher list for a shift in the proccessing day
            for shift in day_shifts:
                class_list[shift] = [cl for cl in self.classes
                                     if shift in cl.time_frames]
                teacher_list[shift] = available_teachers


            #ALLOCATIONS:
            for shift in day_shifts:
                if len(teacher_list[shift]) < len(class_list[shift]):
                    return False #'not enough teachers for this case'

                # sort the class_list based on native percentage
                temp_list_to_reorder_classes = [cl.get_native_need_rate() for cl in class_list[shift]]
                class_list[shift] = [cl for temp,cl in sorted(zip(temp_list_to_reorder_classes, class_list[shift]), key=lambda pair: pair[0])]

                # allocate native teachers to their classes: regular or smartchoice based of the need of native rate
                for cl in class_list[shift]:
                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place native teacher to their main classes if possible, if not => next
                        if cl.teacher is teacher and teacher.type=='ntfulltime':
                            if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher in SC classes
                                temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_native_lesson_count()
                                cl.increase_learned_lesson_number()
                                teacher.lesson_count += 1
                                break

                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if this teacher done
                        # place native teacher to any in-need class
                        if teacher.type in ['ntfulltime','ntparttime']:
                            if cl.get_native_need_rate() < 100: # calcuate the percentage of native teacher 
                                temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_native_lesson_count()
                                cl.increase_learned_lesson_number()
                                teacher.lesson_count += 1
                                break

                    # after this allocation, native teachers might not be allocated to any classes because the need rate is high
                    # need to allocate these teachers later


                # allocate full time and part time vietnamese teachers to their classes: regular based of the need of vn rate
                for cl in class_list[shift]:
                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place full time vietnamese teacher to their main classes
                        if cl.teacher is teacher and teacher.type=='vnfulltime':
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_main_vn_teacher_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break

                    
                        if cl.teacher is teacher and teacher.type=='vnparttime':
                            if cl.get_main_vn_teacher_need_rate() < 66.7: #100*2/3 calcuate the percentage of vn partime main teacher in regular classes
                                temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                                class_teacher_allocations[shift].append(temp)
                                cl.increase_main_vn_teacher_lesson_count()
                                cl.increase_learned_lesson_number()
                                teacher.lesson_count += 1
                                break
                
                # allocate full time native teachers to their classes, dont care about any rate
                for cl in class_list[shift]:
                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place native teacher to their main classes if possible, if not => next
                        if cl.teacher is teacher and teacher.type == 'ntfulltime':
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_native_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break
            

                #==============================================
                # allocate teachers left to classes
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
                    if not any(cl.class_name in string for string in class_teacher_allocations[shift]): # check if this class done
                        remaining_classes.append(cl)


                # get list of classes which have main teacher as parttime
                temp_classes_for_part_time_teachers = []
                temp_parttime_teachers_allocation = []
                for cl in remaining_classes:
                    for teacher in remaining_teachers:
                        if cl.teacher is teacher:
                            temp_classes_for_part_time_teachers.append(cl)
                            temp_parttime_teachers_allocation.append(teacher)
                            break


                # arrange remaining full time teachers to remaining classes which dont have main teacher 
                for cl in remaining_classes:
                    if cl not in temp_classes_for_part_time_teachers:
                        proper_teachers = []
                        for teacher in remaining_teachers:
                            if cl.class_name not in teacher.improper_class_names and teacher not in temp_parttime_teachers_allocation:
                                if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                                    proper_teachers.append(teacher)
                    
                        least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnfulltime')
                        if least_busy_teacher!=None:
                            temp = 'arrange remaining full time teachers to remaining classes which dont have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1



                # arrange remaining part time teachers remaining classes which dont have main teacher 
                for cl in remaining_classes:
                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    if cl not in temp_classes_for_part_time_teachers:
                        proper_teachers = []
                        for teacher in remaining_teachers:
                            if cl.class_name not in teacher.improper_class_names and teacher not in temp_parttime_teachers_allocation:
                                if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                                    proper_teachers.append(teacher)

                        least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnparttime')
                        if least_busy_teacher!=None:

                            temp = 'arrange remaining part time teachers remaining classes which dont have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1

                # TODO: 


                # arrange remaining full time teachers to partime classes which have main teacher 
                # todo: get check which class is proper to take back (random or priority)
                for cl in temp_classes_for_part_time_teachers:
                    proper_teachers = []
                    for teacher in remaining_teachers:
                        if cl.class_name not in teacher.improper_class_names:
                            if not any(teacher.name in string for string in class_teacher_allocations[shift]):
                                proper_teachers.append(teacher)
                    
                    least_busy_teacher = self.get_least_busy_teacher(proper_teachers, 'vnfulltime')
                    if least_busy_teacher!=None:
                        temp = 'arrange remaining full time teachers to partime classes which have main teacher ' + cl.class_name + ' - ' +least_busy_teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)
                        cl.increase_learned_lesson_number()
                        teacher.lesson_count += 1


                # allocate part time vietnamese teachers to their classes remaining:
                for cl in class_list[shift]:
                    if any(cl.class_name in string for string in class_teacher_allocations[shift]): continue # check if this class done
                    for teacher in teacher_list[shift]:
                        if any(teacher.name in string for string in class_teacher_allocations[shift]): continue # check if teacher done
                        # place full time vietnamese teacher to their main classes
                        if cl.teacher is teacher:
                            temp = cl.class_name + ' - ' +teacher.name + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                            class_teacher_allocations[shift].append(temp)
                            cl.increase_main_vn_teacher_lesson_count()
                            cl.increase_learned_lesson_number()
                            teacher.lesson_count += 1
                            break

                # teachers and classes left after apply filters above
                for teacher in teacher_list[shift]:
                    if not any(teacher.name in string for string in class_teacher_allocations[shift]): # check if teacher done
                        class_teacher_allocations[shift].append('redundant teacher: ' + teacher.name)
                for cl in class_list[shift]:
                    if not any(cl.class_name in string for string in class_teacher_allocations[shift]): # check if this class done
                        temp = 'unprocessed class: ' + cl.class_name  + ' - native: ' + str(cl.get_native_need_rate()) + ' - main vn: ' + str(cl.get_main_vn_teacher_need_rate())
                        class_teacher_allocations[shift].append(temp)

        return class_teacher_allocations


    def calculate_assessments(self, schedule):
        # get list of strings of teacher + main class, native teachers:
        main_teachers_classes_list = []
        native_teachers_classes_list = []
        parttime_teachers_classes_list = []
        fulltime_teachers_classes_list = []
        asssessments = {}
        for teacher in self.teachers:
            for cl in get_teacher_main_classes(teacher):
                main_teachers_classes_list.append(cl.class_name +' - '+ teacher.name)
            if teacher.type in ['ntfulltime', 'ntparttime']:
                native_teachers_classes_list.append(teacher.name)
            if teacher.type=='vnparttime':
                parttime_teachers_classes_list.append(teacher.name)
            if teacher.type=='vnfulltime':
                fulltime_teachers_classes_list.append(teacher.name)

            
        # filter unwanted string in schedule flat list
        schedule_flat_list = [item for sublist in schedule.values() for item in sublist]

        asssessments['is not done'] = any('unprocessed class' in string for string in schedule_flat_list)


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
        
        #print('number of lessons for each vn fulltime teacher:')
        lesson_counts = []
        for each_string in fulltime_teachers_classes_list:
            get_teacher_by_name(each_string).lesson_count = sum(each_string in s for s in schedule_flat_list)
            if get_teacher_by_name(each_string).type!='asup':
                lesson_counts.append(get_teacher_by_name(each_string).lesson_count )
            #print(each_string, get_teacher_by_name(each_string).lesson_count)
        

        
        asssessments['native usage'] = native_teacher_count/len(schedule_flat_list)
        asssessments['main teacher'] = right_teacher_count/len(schedule_flat_list)
        asssessments['parttime usage'] = parttime_teacher_count/len(schedule_flat_list)
        asssessments['teacher work balance'] = max(lesson_counts) - min(lesson_counts) # the less the better
        
        return asssessments




# todo: asup không ưu tiên dạy
# todo: xử lý off combinations đầu vào => chạy từng ngày xem đo tối ưu
# todo: 


    def print_schedule(self, schedule):
        self.calculate_assessments(schedule)
        for shift in self.shifts:
            #continue # note: ngung print de test
            try:
                for each in schedule[shift]:
                    print(shift, each)
                    pass
                print('\n')
                pass
            except Exception as e:
                pass

        print('\n')

    def find_best_schedule(self):
        i=0
        s = time.time()
        number_of_combinations, off_combinations = self.create_off_combinations()
        for off_combination in off_combinations:

            s = time.time()

            #print(off_combination)
            result_schedule = self.put_schedule(off_combination)
            if result_schedule!=False:

                # print only native
                for each in off_combination:
                    if 'Andre' in ','.join(each) or 'Matt' in ','.join(each):
                        print(each)

                self.print_schedule(result_schedule)
                i+=1
                
                if i==10: break

            #print(i, number_of_combinations)
            #print(time.time()-s, )


