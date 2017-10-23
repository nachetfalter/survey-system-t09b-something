'''
unittests/test_models.py
- - - - - - -
models part unit test
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import unittest

from datetime import datetime
from flask import url_for
from sqlalchemy import exc
from app import initialize_app, sqlalchemy as db
from app.model.models import User, Course, Survey, Question, \
                             Survey_Question, Choice, Enrolment


class SurveyTest(unittest.TestCase):

    ''' Test Survey Operation in DB '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        course_id = Course.new('COMP1531', '17s2')
        Survey.new(course_id, "test survey",
                   datetime(2016, 10, 20, 0, 0), datetime(2016, 10, 21, 0, 0))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_survey_creation(self):
        ''' check whether survey created in setUp function '''
        self.assertIsNotNone(Survey.query.filter_by(name="test survey").first())

    def test_survey_creation_error(self):
        ''' check whether errors will be raised when inserting wrong data '''
        with self.assertRaises((TypeError, exc.StatementError)):
            Survey.new("0", "0", "0", "0")

    def test_survey_modification(self):
        ''' check whether survey created in setUp function can be modified '''
        test_survey = Survey.query.filter_by(name="test survey").first()
        Survey.update(test_survey.sID, test_survey.cID, "revised test survey",
                      datetime(2017, 10, 22, 0, 0), datetime(2017, 10, 23, 0, 0))
        self.assertEqual(Survey.query.filter_by(name="revised test survey").first(),
                         Survey.query.filter_by(start_date=datetime(2017, 10, 22, 0, 0)).first())

    def test_survey_deletion(self):
        ''' check whether a new survey can be deleted '''
        course_id = Course.new('COMP1531', '18s1')
        survey_id = Survey.new(course_id, "another test survey",
                               datetime(2017, 10, 25, 0, 0), datetime(2017, 10, 26, 0, 0))
        self.assertIsNotNone(Survey.query.filter_by(cID=course_id).first())
        Survey.delete(survey_id)
        self.assertIsNone(Survey.query.filter_by(cID=course_id).first())

    def test_survey_add_question(self):
        ''' check whether question can be added to survey '''
        course_id = Course.query.filter_by(course='COMP1531', sem='17s2').first().cID
        question_id = Question.new('Gne', "one test question")
        survey_id = Survey.query.filter_by(cID=course_id).first().sID
        survey_question_id = Survey_Question.new(survey_id, question_id, 1)
        survey_question = Survey_Question.load(survey_question_id)
        self.assertIsNotNone(survey_question)
        self.assertEqual(survey_question.qtype, 'Gne')
        self.assertEqual(survey_question.title, "one test question")

    def test_survey_remove_question(self):
        ''' check whether question can be removed from survey '''
        course_id = Course.query.filter_by(course='COMP1531', sem='17s2').first().cID
        survey_id = Survey.new(course_id, "another test survey",
                               datetime(2017, 10, 25, 0, 0), datetime(2017, 10, 26, 0, 0))
        question_id = Question.new('Gne', "another test question")
        survey_question_id = Survey_Question.new(survey_id, question_id, 1)
        survey_question = Survey_Question.load(survey_question_id)
        self.assertIsNotNone(survey_question)
        Survey_Question.delete(survey_question_id)
        self.assertIsNone(Survey_Question.load(survey_question_id))


class QuestionTest(unittest.TestCase):

    ''' Test Question Operation in DB '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Question.new('Gne', "test question")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_gne_question_creation(self):
        ''' check whether general question created in setUp function '''
        self.assertEqual(Question.query.filter_by(title="test question").first().qtype,
                         'Gne')

    def test_opt_question_creation(self):
        ''' check whether optional question can be created '''
        Question.new('Opt', "another test question")
        self.assertEqual(Question.query.filter_by(title="another test question").first().qtype,
                         'Opt')

    def test_choice_creation(self):
        ''' check whether choices can be added to question '''
        question = Question.query.filter_by(title="test question").first()
        Choice.new(question.qID, "first choice", 1)
        Choice.new(question.qID, "second choice", 2)
        Choice.new(question.qID, "third choice", 3)
        self.assertIsNotNone(question.extract().pop('cho_con'))


class UserTest(unittest.TestCase):

    ''' Test User Operation in DB '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        ''' check whether user can be created '''
        User.new("test_user", "password", 'Staff')
        self.assertIsInstance(User.load("test_user"), User)

    def test_student_enrolment(self):
        ''' check whether student can be enrolled '''
        User.new("z2333333", "password", 'Student')
        course_id = Course.new('COMP1531', '17s2')
        Enrolment.new("z2333333", course_id)
        self.assertIsInstance(User.load("z2333333"), User)
        self.assertIsInstance(Course.load(course_id), Course)
        self.assertIsInstance(Enrolment.query.filter_by(zID="z2333333", cID=course_id).first(),
                              Enrolment)
