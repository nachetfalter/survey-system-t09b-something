'''
app/main/validators.py
- - - - - - -
server-side data validators for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''

import dateutil

from ..model.models import Survey, Course, Result, Survey_Question


class Validator:

    ''' collection of data validators '''

    @staticmethod
    def survey_answer(surv_id, answer_data):
        ''' survey answer return data validator '''
        ques_num = len(Survey.load(surv_id).extract().pop('sqID'))
        if answer_data.get('username', None) is None:
            return False
        if len(answer_data.get('choice_id')) == len(answer_data.get('question_id')) == \
            len(answer_data.get('answer')) == ques_num:
            for i in range(0, ques_num):
                choice = Result.load(answer_data.get('choice_id')[i])
                if choice is None:
                    return False
                if choice.order != 0 and answer_data.get('answer')[i] != "1":
                    return False
                if Survey_Question.load(answer_data.get('question_id')[i]) is None:
                    return False
            if not Validator.survey_offline(surv_id):
                return True
        return False

    @staticmethod
    def survey_edit(survey_data):
        ''' survey modification return data validator '''
        if survey_data.get('survey_name') is not None:
            if Course.load(survey_data.get('course_id')) is None:
                return False
            try:
                dateutil.parser.parse(survey_data.get('start_date'))
            except ValueError:
                return False
            try:
                dateutil.parser.parse(survey_data.get('close_date'))
            except ValueError:
                return False
        return True

    @staticmethod
    def survey_new(survey_data):
        ''' survey creation return data validator '''
        if Course.load(survey_data.get('course_id')) is None:
            return False
        try:
            dateutil.parser.parse(survey_data.get('start_date'))
        except ValueError:
            return False
        try:
            dateutil.parser.parse(survey_data.get('close_date'))
        except ValueError:
            return False
        return True

    @staticmethod
    def question_edit(question_data):
        ''' question modification return data validator '''
        if question_data.get('question_type') not in ['Gne', 'Opt']:
            return False
        return True

    @staticmethod
    def question_new(question_data):
        ''' question creation return data validator '''
        if question_data.get('question_type') not in ['Gne', 'Opt']:
            return False
        return True

    @staticmethod
    def survey_offline(survey_id):
        ''' check survey offline or not '''
        survey = Survey.load(survey_id)
        if survey.status == 1:
            return False
        return True
