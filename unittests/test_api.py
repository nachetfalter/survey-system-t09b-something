'''
unittests/test_api.py
- - - - - - -
api part unit test
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import json
import unittest

from flask import url_for
from app import initialize_app, sqlalchemy as db
from app.auth.api import get_token_user
from app.model.models import User


class APIUserTest(unittest.TestCase):

    ''' Test User API '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        User.new('z2333333', 'password', 'Admin')
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_api(self):
        ''' test user api '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333333",
            password="password"
            )), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        token = json.loads(resp.data.decode('UTF-8')).get('token', None)
        self.assertIsNotNone(token)
        self.assertEqual(get_token_user(token).zID, "z2333333")

    def get_header(self, username, password):
        ''' helper function to generate header '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username=username,
            password=password
            )), content_type="application/json")
        return {
            'Authorization': 'Bearer ' + json.loads(resp.data.decode('UTF-8')).get('token'),
            'Accept': 'application/json'
        }


class APISurveyTest(unittest.TestCase):

    ''' Test Survey API '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        User.new('z2333333', 'password', 'Admin')
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ad_survey_list_api(self):
        ''' test admin survey list api '''
        resp = self.client.get(url_for('main.survey_all_api'),
                               headers=APIUserTest.get_header(self, "z2333333", "password"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('surveys', json.loads(resp.data.decode('UTF-8')))
