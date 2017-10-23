'''
app/auth/views.py
- - - - - - -
webpage routes for package 'auth' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import render_template, request, url_for
from flask_login import login_user, logout_user, login_required

from . import auth
from .api import get_token_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    login page
    only token is accepted
    '''
    if request.is_json:
        json_data = request.json
        user = get_token_user(json_data.get('token'))
        role = user.auth
        login_user(user)
        if role == 'Admin':
            return request.args.get('next') or url_for('main.admin_dashboard')
        elif role == 'Staff':
            return request.args.get('next') or url_for('main.staff_dashboard')
        return request.args.get('next') or url_for('main.student_dashboard')
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    '''
    logout route, may be considered as an api
    '''
    logout_user()
    return url_for('.login')
