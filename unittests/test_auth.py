'''
unittests/test_auth.py
- - - - - - -
auth part unit test
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import json
import unittest

from flask import url_for
from app import initialize_app, sqlalchemy as db
from app.model.models import User


class AdminAuthTest(unittest.TestCase):

    ''' Test Admin Auth '''

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

    def test_admin_auth(self):
        ''' simulate admin login process '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333333",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        self.assertEqual(test_resp.data.decode('UTF-8'), url_for('main.admin_dashboard'))

    def test_admin_auth_forbidden(self):
        ''' check whether admin is able to access staff/student dashboard '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333333",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        resp = self.client.get(url_for('main.staff_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get(url_for('main.student_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)


class StaffAuthTest(unittest.TestCase):

    ''' Test Staff Auth '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        User.new('z2333334', 'password', 'Staff')
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_staff_auth(self):
        ''' simulate staff login process '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333334",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        self.assertEqual(test_resp.data.decode('UTF-8'), url_for('main.staff_dashboard'))

    def test_staff_auth_forbidden(self):
        ''' check whether staff is able to access admin/student dashboard '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333334",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        resp = self.client.get(url_for('main.admin_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get(url_for('main.student_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)


class StudentAuthTest(unittest.TestCase):

    ''' Test Student Auth '''

    def setUp(self):
        self.app = initialize_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        User.new('z2333335', 'password', 'Student')
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_student_auth(self):
        ''' simulate student login process '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333335",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        self.assertEqual(test_resp.data.decode('UTF-8'), url_for('main.student_dashboard'))

    def test_student_auth_forbidden(self):
        ''' check whether student is able to access admin/staff dashboard '''
        resp = self.client.post(url_for('auth.gen_token'), data=json.dumps(dict(
            username="z2333335",
            password="password"
            )), content_type="application/json")
        test_resp = self.client.get(
            url_for('auth.login'), data=json.dumps(dict(
                token=json.loads(resp.data.decode('UTF-8')).get('token')
            )), content_type="application/json")
        resp = self.client.get(url_for('main.admin_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)
        resp = self.client.get(url_for('main.staff_dashboard'), follow_redirects=True)
        self.assertEqual(resp.status_code, 403)
