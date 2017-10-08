'''
deploy.py
- - - - - - -
script that import data into database for the website
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


import os
import sys
import csv

from app import initialize_app, sqlalchemy as db


# TODO to be improved

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def csv_read(f_name):
    r_data = list()
    try:
        csv_f = open(f_name, 'r')
    except FileNotFoundError:
        print(u"Please prepare data file for importing.")
        sys.exit(1)
    except Exception:
        print(u"电脑瓦特了")
        sys.exit(1)
    reader = csv.reader(csv_f)
    for row in reader:
        r_data.append(row)
    csv_f.close()
    return r_data


if len(sys.argv) == 2 and \
        sys.argv[1] in ['development', 'testing', 'production', 'default']:
    config = sys.argv[1]
else:
    print("Usage: python3 deploy.py [development|testing|production|default]")
    sys.exit(1)


initialize_app(config).app_context().push()
    
from app.model import models

db.create_all()

courses_path = BASEDIR + '/data/courses.csv'
for row in csv_read(courses_path):
    models.Course.new(row[0], row[1])

users_path = BASEDIR + '/data/passwords.csv'
for row in csv_read(users_path):
    models.User.new(row[0], row[1], row[2].title())

enrolment_path = BASEDIR + '/data/enrolments.csv'
for row in csv_read(enrolment_path):
    cid = models.Course.query.filter_by(course=row[1], sem=row[2]).first().cID
    models.Enrolment.new(row[0], cid)
