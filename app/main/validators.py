'''
app/main/validators.py
- - - - - - -
server-side data validators for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''

from ..model.models import Survey


# TODO to be implemented


class Validator:

    @staticmethod
    def survey_answer(surv_id, answer_data):
        return True

    @staticmethod
    def survey_edit(survey_data):
        return True

    @staticmethod
    def survey_new(survey_data):
        return True

    @staticmethod
    def question_edit(question_data):
        return True

    @staticmethod
    def question_new(question_data):
        return True

    @staticmethod
    def survey_offline(survey_id):
        survey = Survey.load(survey_id)
        if survey.status == 0:
            return True
        return False


