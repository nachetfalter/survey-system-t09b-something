'''
admin/__init__.py
- - - - - - -
initialization of module 'admin' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-09
'''

from flask import Blueprint

main = Blueprint('main', __name__, template_folder="main")

from . import api, views, errors
