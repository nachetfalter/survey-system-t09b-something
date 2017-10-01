# Title: Models.py
# Author: Victor Wang
# The basic behaviors are:
# when a user is deleted, his enrolment is deleted, and that's it
# when a question in the question pool is deleted:
# the respective choice content of this question is also deleted,
# but that's it.
# when a survey is deleted, the questions in it are all deleted,
# its result and the result record of this survey are also deleted
# But you shouldn't worry about any of these above,
# because I will do the cascade internally.

from sqlalchemy import CheckConstraint, event
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin
from datetime import datetime
from .. import sqlalchemy as db, bcrypt, login_manager


def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')


event.listen(db.engine, 'connect', _fk_pragma_on_connect)


# Pass either one key or a list of keys
def db_load(table, key):
    if isinstance(key, list) is False:
        if key is None:
            return table.query.all()
        else:
            return table.query.get(key)
    else:
        if key[0] is None and key[1] is None:
            return table.query.all()
        else:
            return table.query.get(key)


# Load User
@login_manager.user_loader
def load_user(zID):
    return User.load(zID)


# User contains all three types of operators.
# The zID is a varchar which can take both the zid and the user name,
# eid is the enrolment ID
class User(db.Model, UserMixin):

    __tablename__ = "User"
    zID = db.Column("zID", db.Text, primary_key=True, autoincrement=False)
    _password = db.Column("password", db.Binary(60), nullable=False)
    auth = db.Column("auth", db.String(7), CheckConstraint('auth == "Student" or auth == "Admin" or auth == "Staff"'))

    def __init__(self, zID, password_text, auth):
        self.zID = zID
        self.password = password_text
        self.auth = auth

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_pass(self, password_text):
        self._password = bcrypt.generate_password_hash(password_text)

    @hybrid_method
    def verify_password(self, password_text):
        return bcrypt.check_password_hash(self.password, password_text)

    def get_id(self):
        return self.zID

    @staticmethod
    def new(zID, password, auth):
        result = User(zID, password, auth)
        db.session.add(result)
        db.session.commit()

    @staticmethod
    def load(zID=None):
        return db_load(User, zID)

    # This method will return all elements in User as a dict with a new element 'cID'
    # Which contains all courses id this user is enrolled in. Admin has none.
    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        course = Enrolment.query.filter_by(zID=self.zID).all()
        if len(course) == 0:
            dic['cID'] = []
            dic['course'] = []
            return dic
        else:
            cID = []
            course = []
            for i in course:
                cID.append(i.cID)
                course.append(i.course)
            dic['cID'] = cID
            dic['course'] = course
            return dic

    # Boolean check the authority of the user.
    def check_auth(self, auth):
        if self.auth != auth and self.auth != 'Admin':
            return 0
        else:
            return 1

    # Delete a user will also delete the enrolment record associate with
    # it
    @staticmethod
    def delete(zID):
        data = db_load(User, zID)
        db.session.delete(data)
        db.session.commit()

    @staticmethod
    def update(zID, password, auth):
        target = User.query.get(zID)
        target.password = password
        target.auth = auth
        db.session.commit()


# This is a minor class built as a bridge entity
# to resolve the mn relationship between users and courses.
# The reason why there is no update in
# this is because once the enrolment period
# past, instead of renew, the record would be deleted
# You shouldn't even use the load in this to load an enrolment record,
# but instead using the relationship I made in User
# Weak entity
class Enrolment(db.Model):

    __tablename__ = "Enrolment"
    zID = db.Column("zID", db.Text, db.ForeignKey('User.zID', ondelete='CASCADE'), primary_key=True)
    cID = db.Column("cID", db.Integer, db.ForeignKey('Course.cID', ondelete='CASCADE'), primary_key=True)

    def __init__(self, zID, cID):
        self.zID = zID
        self.cID = cID

    @staticmethod
    def new(zID, cID):
        result = Enrolment(zID, cID)
        db.session.add(result)
        db.session.commit()

    @staticmethod
    def load(zID, cID):
        return db_load(Enrolment, [zID, cID])


# sem is the semester of the course, you shouldn't need to load the
# content of this class outside of the pk anyway.
# Same thing, one does not simply update the course.
# They are either added or deleted
class Course(db.Model):

    __tablename__ = "Course"
    cID = db.Column("cID", db.Integer, primary_key=True, autoincrement=True)
    course = db.Column("course", db.String(8), nullable=False)
    sem = db.Column("sem", db.String(4), nullable=False)

    def __init__(self, course, sem):
        self.course = course
        self.sem = sem

    @staticmethod
    def new(course, sem):
        result = Course(course, sem)
        db.session.add(result)
        db.session.commit()
        return result.cID

    @staticmethod
    def load(cID=None):
        return db_load(Course, cID)

    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        return dic

    # Delete a course will also delete the enrolment record associate with
    # it
    @staticmethod
    def delete(cID):
        data = db_load(Course, cID)
        db.session.delete(data)
        db.session.commit()


#qtype is about whether this question is considered as a generic question or
#a optional question. The title of the question has a limit of 80 characters
class Question(db.Model):

    __tablename__ = "Question"
    qID = db.Column("qID", db.Integer, primary_key=True, autoincrement=True)
    qtype = db.Column("qtype", db.String(3), CheckConstraint('qtype == "Opt" or qtype == "Gne"'), default='Gne')
    title = db.Column("title", db.String(80), nullable=False)
    cho_num = db.Column("cho_num", db.Integer, default=0)

    def __init__(self, qtype, title, cho_num):
        self.qtype = qtype
        self.title = title
        self.cho_num = cho_num

    @staticmethod
    def new(qtype, title, cho_num):
        result = Question(qtype, title, cho_num)
        db.session.add(result)
        db.session.commit()
        return result.qID

    @staticmethod
    def load(qID=None):
        return db_load(Question, qID)

    # Choice ID will be added to this dict under the key 'choice'
    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        choice = Choice.query.filter_by(qID=self.qID).all()
        order = 1
        switch = 0
        if len(choice) == 0:
            dic['chID'] = []
            dic['cho_con'] = []
        elif choice.order == 0:
            chID = []
            cho_con = []
            chID.append(choice.chID)
            cho_con.append(choice.cho_con)
            dic['chID'] = chID
            dic['cho_con'] = cho_con
        else:
            chID = []
            cho_con = []
            while switch == 0:
                switch = 1
                for i in choice:
                    if i.order == order:
                        chID.append(i.chID)
                        cho_con.append(i.cho_con)
                        order += 1
                        switch = 0
            dic['chID'] = chID
            dic['cho_con'] = cho_con
        return dic

    @staticmethod
    def cho_num(qID):
        buff = []
        buff.extend(Choice.query.filter_by(qID=qID).all())
        return len(buff)

    # Delete a question will cause the choices associate with it to be deleted
    @staticmethod
    def delete(qID):
        data = db_load(Question, qID)
        db.session.delete(data)
        db.session.commit()

    @staticmethod
    def update(qID, qtype, title, cho_num):
        target = Question.query.get(qID)
        target.qtype = qtype
        target.title = title
        target.cho_num = cho_num
        db.session.commit()


#Choice is also a bridge entity used to break the mn relationship between
#question and its choice contents. cho_con = choice content
#Weak entity
class Choice(db.Model):

    __tablename__ = "Choice"
    chID = db.Column("chID", db.Integer, primary_key=True, autoincrement=True)
    qID = db.Column("qID", db.Integer, db.ForeignKey('Question.qID', ondelete='CASCADE'))
    cho_con = db.Column("cho_con", db.Text)
    order = db.Column("order", db.Integer)

    def __init__(self, qID, cho_con, order):
        self.qID = qID
        self.cho_con = cho_con
        self.order = order

    # This method return the choice ID only
    @staticmethod
    def new(qID, cho_con, order):
        result = Choice(qID, cho_con, order)
        db.session.add(result)
        question = Question.load(qID)
        question.cho_num += 1
        db.session.commit()
        return result.chID

    @staticmethod
    def load(chID=None):
        return db_load(Choice, chID)

    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        return dic

    # If chID is not defined, all choices of this question will be deleted
    @staticmethod
    def delete(chID):
        data = db_load(Choice, chID)
        db.session.delete(data)
        db.session.commit()

    @staticmethod
    def update(chID, cho_con, order):
        target = Choice.query.get(chID)
        target.cho_con = cho_con
        target.order = order
        db.session.commit()


#Con is a boolean indicate whether the survey is online or not
class Survey(db.Model):

    __tablename__ = "Survey"
    sID = db.Column("sID", db.Integer, primary_key=True, autoincrement=True)
    cID = db.Column("cID", db.Integer, db.ForeignKey('Course.cID', ondelete='CASCADE'))
    name = db.Column("name", db.Text, nullable=False)
    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow())
    start_date = db.Column("start_date", db.DateTime)
    update_date = db.Column("update_date", db.DateTime, default=datetime.utcnow())
    close_date = db.Column("close_date", db.DateTime)
    status = db.Column("status", db.Boolean, default=False)

    def __init__(self, cID, name, start_date, close_date):
        self.cID = cID
        self.name = name
        self.start_date = start_date
        self.close_date = close_date

    @staticmethod
    def new(cID, name, start_date, close_date):
        result = Survey(cID, name, start_date, close_date)
        db.session.add(result)
        db.session.commit()
        return result.sID

    @staticmethod
    def load(sID=None):
        return db_load(Survey, sID)

    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        question = Survey_Question.query.filter_by(sID=self.sID).all()
        order = 1
        switch = 0
        if len(question) == 0:
            dic['sqID'] = []
            return dic
        else:
            sqID = []
            while switch == 0:
                switch = 1
                for i in question:
                    if i.order == order:
                        sqID.append(i.sqID)
                        order += 1
                        switch = 0
            dic['sqID'] = sqID
            return dic

    @staticmethod
    def delete(sID):
        data = db_load(Survey, sID)
        db.session.delete(data)
        db.session.commit()

    # This method push the survey online
    @staticmethod
    def status_operation(sID):
        data = db_load(Survey, sID)
        if data.status is True:
            data.status = False
        else:
            data.status = True
        db.session.commit()

    @staticmethod
    def update(sID, cID, name, start_date, close_date):
        target = Survey.query.get(sID)
        target.name = name
        target.cID = cID
        target.start_date = start_date
        target.close_date = close_date
        target.update_date = datetime.utcnow()
        db.session.commit()


#Answer record is used to prevent the same person from doing the survey again.
#Record is a boolean which indicates whether this person has done the survey
#You shouldn't touch the methods here as it is for internal use.
#Weak entity
class Answer_Record(db.Model):

    __tablename__ = "Answer_Record"
    zID = db.Column("zID", db.Text, db.ForeignKey('User.zID', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    sID = db.Column("cID", db.Integer, db.ForeignKey('Survey.sID', ondelete='CASCADE'), primary_key=True, autoincrement=False)

    def __init__(self, zID, sID):
        self.zID = zID
        self.sID = sID

    @staticmethod
    def new(zID, sID):
        result = Answer_Record(zID, sID)
        db.session.add(result)
        db.session.commit()

    # There is no reason what so ever you should need load or extract this class
    # Therefore I only added one for you to check for record and return Boolean
    @staticmethod
    def check(zID, sID):
        target = db_load(Answer_Record, [zID, sID])
        if target is None:
            return False
        else:
            return True


#Survey question is used to store questions in surveys to avoid situation where
#certain questions are deleted from the question pool.
class Survey_Question(db.Model):

    __tablename__ = "Survey_Question"
    sqID = db.Column("sqID", db.Integer, primary_key=True, autoincrement=True)
    sID = db.Column("sID", db.Integer, db.ForeignKey('Survey.sID', ondelete='CASCADE'))
    qtype = db.Column("qtype", db.String(3), CheckConstraint('qtype == "Opt" or qtype == "Gne"'))
    title = db.Column("title", db.String(80), nullable=False)
    cho_num = db.Column("cho_num", db.Integer, default=0)
    order = db.Column("order", db.Integer)

    def __init__(self, sID, qtype, title, cho_num, order):
        self.sID = sID
        self.qtype = qtype
        self.title = title
        self.cho_num = cho_num
        self.order = order

    @staticmethod
    def new(sID, qtype, title, cho_num, order):
        result = Survey_Question(sID, qtype, title, cho_num, order)
        db.session.add(result)
        db.session.commit()
        return Survey_Question.sqID

    @staticmethod
    def load(sqID=None):
        return db_load(Survey_Question, sqID)

    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        choice = Result.query.filter_by(sqID=self.sqID).all()
        order = 1
        switch = 0
        if len(choice) == 0:
            dic['chID'] = []
            dic['cho_con'] = []
        elif choice.order == 0:
            chID = []
            cho_con = []
            chID.append(choice.chID)
            cho_con.append(choice.cho_con)
            dic['chID'] = chID
            dic['cho_con'] = cho_con
        else:
            chID = []
            cho_con = []
            while switch == 0:
                switch = 1
                for i in choice:
                    chID.append(i.chID)
                    cho_con.append(i.cho_con)
                    order += 1
                    switch = 0
            dic['chID'] = chID
            dic['cho_con'] = cho_con
        return dic

    @staticmethod
    def cho_num(sqID):
        buff = []
        buff.extend(Result.query.filter_by(sqID=sqID).all())
        return len(buff)

    @staticmethod
    def delete(sqID=None):
        data = db_load(Survey_Question, sqID)
        db.session.delete(data)
        db.session.commit()

    @staticmethod
    def update(sqID, title, cho_num, order):
        target = Survey_Question.query.get(sqID)
        target.title = title
        target.cho_num = cho_num
        target.order = order
        db.session.commit()


#Result not only contains the answer to questions used in the survey but it also
#contains the content of the choices. In the case of text based question.
#chID increment with each answer, but the cho_con is nothing, and the answer is
#the respective string.
#Derived entity
class Result(db.Model):

    __tablename__ = "Result"
    chID = db.Column("chID", db.Integer, primary_key=True, autoincrement=True)
    sqID = db.Column("sqID", db.Integer, db.ForeignKey('Survey_Question.sqID', ondelete='CASCADE'))
    cho_con = db.Column("cho_con", db.Text)
    order = db.Column("order", db.Integer)
    answer = db.Column("answer", db.Text, default='Null')

    def __init__(self, sqID, cho_con, order, answer):
        self.sqID = sqID
        self.order = order
        self.cho_con = cho_con
        self.answer = answer

    @staticmethod
    def new(sqID, cho_con, order, answer):
        result = Result(sqID, cho_con, order, answer)
        db.session.add(result)
        question = Survey_Question.load(sqID)
        question.cho_num += 1
        db.session.commit()
        return result.chID

    @staticmethod
    def load(chID):
        return db_load(Result, chID)

    def extract(self):
        dic = dict(self.__dict__)
        dic.pop('_sa_instance_state', None)
        if dic['order'] == 0:
            dic['answer'] = dic['answer'].split('औ')
        return dic

    @staticmethod
    def delete(chID):
        data = db_load(Result, [sqID, chID])
        db.session.delete(data)
        db.session.commit()

    # This method is for updating content/order
    @staticmethod
    def update_content(chID, cho_con, order):
        target = Result.query.get(chID)
        target.cho_con = cho_con
        target.order = order
        db.session.commit()

    # This method is for updating the answer
    @staticmethod
    def update_answer(chID, answer):
        target = Result.query.get(chID)
        if target.order != 0:
            target.answer = target.answer + ' + '
            target.answer = eval(target.answer + answer)
        else:
            target.answer = target.answer + 'औ'
            target.answer = target.answer + answer
        db.session.commit()
