import os
from flask_script import Manager, Shell
from app import initialize_app, sqlalchemy as db
from app.model.models import User

app = initialize_app('default')
manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
