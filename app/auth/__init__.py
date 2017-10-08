'''
app/auth/__init__.py
- - - - - - -
initialization of module 'auth' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder="auth")

from . import api, views, errors
