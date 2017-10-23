'''
__init__.py
- - - - - - -
initialization for package 'app' a.k.a. the website
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from apscheduler.schedulers.background import BackgroundScheduler

from config import config


bcrypt = Bcrypt()
mail = Mail()
moment = Moment()
sqlalchemy = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

scheduler = BackgroundScheduler()

def initialize_app(config_name):

    ''' initialize app instance - function factory '''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bcrypt.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    sqlalchemy.init_app(app)
    sqlalchemy.app = app
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
