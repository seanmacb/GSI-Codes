import re
import random
import sys

############################### Function #################################
# Lab groups are randomized for each lab. This script takes a downloaded 
# roster from Canvas and randomly places students in the same section into
# groups, outputting a csv file that can be directly uploaded to Canvas.

############################# Instructions ###############################
# run: python group_randomizer {course num}
# input: downloaded roster from Canvas groups renamed to 'roster.csv' 
######## placed in the same directory
# output: groups.csv in the same directory, can be uploaded directly to 
######### Canvas groups

lab_num = sys.argv[1]

roster_file = open('roster.csv', 'r')
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

# check if students are in two or more sections
if len(double_section_students) > 0:
    print(double_section_students)
    print('these students are listed in two or more sections. fix this before randomizing groups.')
    exit()


# organize student indexes by section to randomize
sections = []
section_student_ind = []

for i in range(1, len(roster)):
    if not section_nums[i-1] in sections:
        sections.append(section_nums[i-1])
        section_student_ind.append([i])
    else:
        section_student_ind[sections.index(section_nums[i-1])].append(i)

# go section by section generating number of groups and students in those groups and randomizing students
for i in range(len(sections)):
    current_section = sections[i]
    num_students = len(section_student_ind[i])
    if int(current_section) < 50:
        num_tables = 10
    else:
        num_tables = 8

    if num_students%3 == 0:
        group_nums = [ 3 ]*int(num_students//3)
    else:
        group_nums = [ 3 ]*int(num_students//3 + 1)
        Iter = 0
        while sum(group_nums)>num_students:
            group_nums[Iter] = group_nums[Iter] - 1
            Iter +=1
    
    group_labels = []
    for j in range(len(group_nums)):
        for k in range(group_nums[j]):
            group_labels.append(j+1)

    random.shuffle(group_labels)

    for j in range(num_students):
        roster[section_student_ind[i][j]].insert(-1, "Section "+current_section+' Lab '+lab_num+' Group '+str(group_labels[j]))


# write out csv file
group_file = open('groups.csv', 'w')

for i in range(1, len(roster)):
    roster[i] = ','.join(roster[i])

group_file.writelines(roster)
group_file.close()
