'''
__init__.py
- - - - - - -
initialization for this project
to be rewritten after the introduce of blueprint
- - - - - - -
ZHENYU YAO z5125769 2017-09
'''

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config['SECRET_KEY'] = 'w235ioj'

Bootstrap(app)
