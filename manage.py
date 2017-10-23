'''
run.py
- - - - - - -
RUN SERVER SCRIPT
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from app import initialize_app, sqlalchemy as db


config = os.environ.get('FLASK_CONFIG') or 'default'
app = initialize_app(config)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    ''' create shell context for app instance '''
    from app.model.models import User, Question, Result, \
                                 Survey, Choice, Survey_Question, \
                                 Enrolment, Answer_Record, Course
    return dict(app=app, db=db, User=User, Question=Question,
                Survey=Survey, Result=Result, Choice=Choice,
                Survey_Question=Survey_Question, Enrolment=Enrolment,
                Answer_Record=Answer_Record, Course=Course)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("migrate_db", MigrateCommand)

try:
    if sys.argv[1] in ['runserver', 'shell']:
        print('===== now using config {} ====='.format(config.upper()))
except IndexError:
    pass

@manager.command
def test():
    ''' run unittests '''
    import unittest
    tests = unittest.TestLoader().discover('unittests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
