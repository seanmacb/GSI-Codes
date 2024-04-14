import re
import matplotlib.pyplot as plt
import sys
from datetime import date
import pandas as pd
import os
import numpy as np

########################### Function ################################
# Compiles grade updates and distribution on a section-by-section
# basis from a canvas exported grade file 

######################### Instructions ##############################
# run: python grades.py {course num}
# input: grades downloaded from Canvas renamed to 'grades.csv' 
### placed in the same directory
# output: displays via matplotlib grading progress and distribution
### on a section-by-section basis



# <B = 0
# B- = 1
# B  = 2
# B+ = 3
# A- = 4
# A  = 5
# A+ = 6


def letter_grade(grade):
    grade = float(grade)
    if grade < 80:
        return 0
    elif 80 <= grade < 84:
        return 1
    elif 84 <= grade < 87:
        return 2
    elif 87 <= grade < 90:
        return 3
    elif 90 <= grade < 94:
        return 4
    elif 94 <= grade < 99:
        return 5
    else:
        return 6

# chunk to return the students with dashes in gradebook
grade_df = pd.read_csv("grades.csv",skiprows=[1,2],skipfooter=1)
grade_df['Section'] = grade_df['Section'].str[-3:]
column_array = []
print("Students with dashes in gradebook\n")
grade_arr = np.array([])
for column in grade_df.columns.values:
    if column.__contains__("Lab") and (not column.__contains__("Score") and (not grade_df[column].isnull().values.all())):
        for student in range(len(grade_df["Student"])):
            if str(grade_df[column][student])=='nan':
                grade_arr = np.append(grade_arr,[column,grade_df["Section"].iloc[student],grade_df["Student"].iloc[student]])
del grade_df,column_array

grade_arr = np.reshape(grade_arr,(-1,3))

sections = np.unique(grade_arr[:,1])
labs = np.unique(grade_arr[:,0])

for section in sections:
    section_arr = grade_arr[grade_arr[:,1]==section]
    print("Section",section)
    print(10*'--')
    for lab in labs:
        if lab in section_arr[:,0]:
            print(lab)
            print(10*'--')
            students = section_arr[section_arr[:,0]==lab][:,2]
            for student in students:
                print(student)
            print()


course_num = sys.argv[1]

grades_file = open('grades.csv', 'r')
grades = grades_file.readlines()[:-1]
grades_file.close()

# get section numbers of students
double_section_students = []
section_nums = []

for i in range(3, len(grades)):
    grades[i] = grades[i].split(',')
    student_section_nums = re.findall('[0-9]+', grades[i][5])[1::2]
    section_nums.append(student_section_nums[0])
    if len(student_section_nums) > 1:
        double_section_students.append(grades[i][0]+','+grades[i][1])

# check if students are in two or more sections
if len(double_section_students) > 0:
    print(double_section_students)
    print('these students are listed in two or more sections. fix this before randomizing groups.')
    exit()

# organize student indexes by section to randomize
sections = []
section_student_ind = []

for i in range(3, len(grades)):
    if not section_nums[i-3] in sections:
        sections.append(section_nums[i-3])
        section_student_ind.append([i])
    else:
        section_student_ind[sections.index(section_nums[i-3])].append(i)

section_student_ind = [ x for _, x in sorted(zip(sections, section_student_ind)) ]
sections = sorted(sections)

grades[0] = grades[0].split(',')
lab_grade_inds = [ grades[0].index(ent)+1 for ent in grades[0] if (('Lab' in ent) and (':' in ent)) ]

fig, axs = plt.subplots((len(sections)+1)//2, 2, sharex=True)
fig.set_figheight(30)
fig.set_figwidth(10)
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)
fig.suptitle(course_num+' Grading Update - '+str(date.today()))

for i in range(len(sections)):
    grading_prog = [0]*len(lab_grade_inds)
    for j in section_student_ind[i]:
        for k in range(len(lab_grade_inds)):
            if not grades[j][lab_grade_inds[k]] == '':
                grading_prog[k] += 100/len(section_student_ind[i])
    
    row = i % ((len(sections)+1)//2)
    col = i // ((len(sections)+1)//2)
    axs[row][col].set_ylabel(sections[i])
    axs[row][col].set_ylim([0,100])
    axs[row][col].bar([ str(i+1) for i in range(len(lab_grade_inds)) ], grading_prog)
    axs[row][col].set_yticks([])
fig.savefig(os.getcwd()+"/"+course_num+"/distribution_"+str(date.today())+".jpg")
plt.show()

current_score_ind = grades[0].index("Current Score") + 1
fig, axs = plt.subplots((len(sections)+1)//2, 2, sharex=True)
fig.set_figheight(30)
fig.set_figwidth(10)
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)
fig.suptitle(course_num+' Grading Distributions - '+str(date.today()))
all_grades = np.array([],dtype=float)

for i in range(len(sections)):
    section_dist = [0]*7
    for j in section_student_ind[i]:
        section_dist[letter_grade(grades[j][current_score_ind])] += 1/len(section_student_ind[i])
    sec_grades = np.array([grades[x] for x in section_student_ind[i]])[:,current_score_ind].astype(float)
    all_grades = np.append(sec_grades,all_grades)
    mean_grades,median_grades = np.mean(sec_grades),np.median(sec_grades)
    row = i % ((len(sections)+1)//2)
    col = i // ((len(sections)+1)//2)
    axs[row][col].set_ylabel(sections[i])
    axs[row][col].set_ylim([0, 1])
    for k in range(7):
        axs[row][col].text(-0.3 + k, 0.8, '{:.2f}'.format(section_dist[k]))
    
    axs[row][col].bar(['<B', 'B-', 'B', 'B+', 'A-', 'A', 'A+'], section_dist)
    axs[row][col].set_yticks([])
    axs[row][col].set_title("Mean: {}, Median: {}".format(np.round(mean_grades,2),np.round(median_grades,2)))
fig.savefig(os.getcwd()+"/"+course_num+"/completion_"+str(date.today())+".jpg")
plt.show()


fig, ax = plt.subplots()

ax.hist(all_grades,np.arange(80,100),alpha=0.5, histtype='bar', ec='black',density=True,stacked=True,align='right')

ax.set_xticks(np.arange(80,100))
ax.set_xlim(80,100)
ax.set_title('Grades in {}'.format(course_num)) 
ax.set_xlabel('Grades') 
ax.set_ylabel('Normalized count [%]')

fig.savefig(os.getcwd()+"/"+course_num+"/allClass_"+str(date.today())+".jpg")

plt.show()