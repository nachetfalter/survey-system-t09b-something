'''
run.py
- - - - - - -
RUN SERVER SCRIPT
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app import initialize_app, sqlalchemy as db

app = initialize_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    from app.model.models import User, Question, Result, Survey
    return dict(app=app, db=db, User=User, Question=Question,
                Survey=Survey, Result=Result)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def db_migrate():
    return MigrateCommand


if __name__ == "__main__":
    manager.run()
