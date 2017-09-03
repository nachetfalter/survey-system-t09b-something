#CSV_Glossary
#Created by: Victor Wang

'''
survey.csv: example: 1 2 3/4/5 "xxx"
surv_ID - PK
course_ID - FK to potential course.csv
question_ID - FK to qustion.csv (must be separated)
surv_name - string, name of the survey

Result.csv: (weak entity) example: 1 2/3/4 2/1/3
surv_ID - PK/FK to Survey.csv
question_ID - PK/FK to Question.csv
result - int 0-9999

Question.csv: example: 1 "xxx" 3 "xxx"/"xxx"/"xxx"
quest_ID - PK
quest - string
choi_num - int
choi_content - string

answer.csv: (weak entity) example: 1/3 1/2/3 2/2/3
u/s_ID - PK      
quest_ID - FK
result - string

admin: example: 1 "xxx"
user_ID - PK
password - string

respondent: example: 1 "xxx"
user_ID - PK
password - string
'''

table = {
    'survey.csv': ['surv_ID','course_ID','ques_ID','surv_name'],
    'result.csv': ['surv_ID','ques_ID','result'],
    'question.csv': ['ques_ID','quest','choi_num','choi_content'],
    'answer.csv': ['s/u_ID','ques_ID','answer'],
    'admin.csv': ['user_ID','password'],
    'res.csv': ['user_ID','password'],
    'courses.csv': ['course_ID']
}
