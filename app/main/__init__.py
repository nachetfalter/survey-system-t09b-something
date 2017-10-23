'''
app/main/__init__.py
- - - - - - -
initialization of module 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''

from flask import Blueprint

main = Blueprint('main', __name__, template_folder="main")

from . import api, views, errors, decorators, schedulers, validators
