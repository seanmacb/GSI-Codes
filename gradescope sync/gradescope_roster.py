import re
import random
import sys

roster_file = open('gs_roster.csv', 'r')
roster = roster_file.readlines()
roster_file.close()

# get section numbers of students
double_section_students = []
section_nums = []

for i in range(1, len(roster)):
    roster[i] = roster[i].split(',')
    student_section_nums = re.findall('[0-9]+', roster[i][5])[1::2]
    section_nums.append(student_section_nums[0])
    if len(student_section_nums) > 1:
        double_section_students.append(roster[i][0]+','+roster[i][1])
    roster[i][5] = student_section_nums[0]+'\n'

# check if students are in two or more sections
if len(double_section_students) > 0:
    print(double_section_students)
    print('these students are listed in two or more sections. fix this before randomizing groups.')
    exit()

# write out csv file
group_file = open('gs_roster.csv', 'w')

for i in range(1, len(roster)):
    roster[i] = ','.join(roster[i])

group_file.writelines(roster)
group_file.close()
