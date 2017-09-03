# Tile: CSV_io.py
# Author: Victor Wang

from csv import DictReader, DictWriter
from .csv_glossary import table
import pathlib
from pathlib import Path

def csv_write(data, f_name):
    col_name = get_col_name(f_name)
    try:
        f = open("./csv/"+f_name, 'r')
        f.close()
    except IOError:
        f = open("./csv/"+f_name, 'w')
    with open("./csv/"+f_name, 'w+') as csv_f:
        writer = DictWriter(csv_f, fieldnames=col_name)
        for i in data:
            writer.writerow(i)
        csv_f.close()

def csv_append(data, f_name):
    col_name = get_col_name(f_name)
    try:
        f = open("./csv/"+f_name, 'r')
        f.close()
    except IOError:
        f = open("./csv/"+f_name, 'w')
    with open("./csv/"+f_name, 'a+') as csv_f:
        writer = DictWriter(csv_f, fieldnames=col_name)
        writer.writerow(data)
        csv_f.close()

def csv_read(f_name):
    col_name = get_col_name(f_name)
    r_data = []
    try:
        file = open("./csv/"+f_name, 'r')
        file.close()
    except IOError:
        file = open("./csv/"+f_name, 'w')
    with open("./csv/"+f_name, 'r+') as csv_f:
        reader = DictReader(csv_f, fieldnames=col_name)
        for row in reader:
            r_data.append(row)
        csv_f.close()
        return r_data

def get_col_name(f_name):
    # some more processing
    return table[f_name]


class Base:
    @classmethod
    def getkey(cls, f_name):
        col_name = get_col_name(f_name)
        return col_name

    @classmethod
    def load(cls, f_name, i_name, inst_id):
        inst = csv_read(f_name)
        inst_id_li = [str(i.get(i_name)) for i in inst]
        if inst_id:
            if inst_id in inst_id_li:
                i = inst_id_li.index(inst_id)
                return inst[i]
            else:
                return None
        else:
            return inst

    @classmethod
    def update(cls, f_name, i_name, inst_id, data):
        inst = csv_read(f_name)
        inst_id_li = [str(i.get(i_name)) for i in inst]
        inst_id = str(inst_id)
        if str(inst_id) not in inst_id_li:
            raise IndexError("Invalid ID")
        else:
            i = inst_id_li.index(inst_id)
            d = inst[i]
            for key in data:
                if key in list(d.keys()):
                    d.update({key: data[key]})
                else:
                    raise KeyError("Invalid Key")
        csv_write(inst, f_name)

    @classmethod
    def append(cls, f_name, i_name, data):
        inst = csv_read(f_name)
        inst_id_li = [int(i.get(i_name)) for i in inst]
        if type(data) is not dict:
            raise TypeError("Dictionary Required")
        new_inst_id = max(inst_id_li, default=0)+1
        if set(list(data.keys())) == set(Base.getkey(f_name)):
            data.update({i_name: new_inst_id})
            csv_append(data, f_name)
        else:
            raise KeyError("Invalid Key")
        return data

    @classmethod
    def delete(cls, f_name, i_name, inst_id):
        inst = csv_read(f_name)
        inst_id_li = [str(i.get(i_name)) for i in inst]
        if inst_id not in inst_id_li:
            raise IndexError("Invalid ID")
        else:
            i = inst_id_li.index(inst_id)
            inst.pop(i)
        csv_write(inst, f_name)


class Survey(Base):

    @staticmethod
    def getkey():
        return super(Survey, Survey).\
            getkey("survey.csv")

    @staticmethod
    def load(survey_id=None):
        if survey_id == None:
            return super(Survey, Survey).\
                load("survey.csv", "surv_ID", None)
        else:
            dic = {}
            dic = super(Survey, Survey).\
                load("survey.csv", "surv_ID", str(survey_id))
            dic['ques_ID'] = dic.get("ques_ID").split("/")
            return dic

    @staticmethod
    def update(data):
        survey_id = ""
        survey_id = data.get("surv_ID")
        data['ques_ID'] = '/'.join(data.get("ques_ID"))
        return super(Survey, Survey).\
            update("survey.csv", "surv_ID", str(survey_id), data)

    @staticmethod
    def append(data):
        data['ques_ID'] = '/'.join(data.get("ques_ID"))
        buff = ''
        buff = data['ques_ID']
        data['surv_ID'] = str(data['surv_ID'])
        dic = {}
        dic = super(Survey, Survey).\
            append("survey.csv", "surv_ID", data)
        Result.append({'surv_ID': dic.get('surv_ID'),'ques_ID': buff,'result': ''})

    @staticmethod
    def delete(survey_id=None):
        Result.delete(str(survey_id))
        return super(Survey, Survey).\
            delete("survey.csv", "surv_ID", str(survey_id))


class Question(Base):

    @staticmethod
    def getkey(choi_num):
        col = []
        col.extend(super(Question, Question).\
            getkey("question.csv"))
        col.pop()
        i = 1
        while i <= choi_num:
            col.append("".join(['choice_',str(i)]))
            i += 1
        return col

    @staticmethod
    def load(ques_id=None):
        if ques_id == None:
            return super(Question, Question).\
                load("question.csv", "ques_ID", ques_id)
        else:
            dic = {}
            dic = super(Question, Question).\
                load("question.csv", "ques_ID", str(ques_id))
            i = 1
            choice = {}
            buf = []
            for j in list(dic.get("choi_content").split("/")):
                buf = "".join(['choice_',str(i)])
                choice[buf] = j
                i += 1
            dic.pop('choi_content')
            dic.update(choice)
            return dic

    @staticmethod
    def update(data):
        ques_id = ""
        ques_id = data.get("ques_ID")
        j = 1
        choice = []
        remove = []
        while j - 1 < len(data) - 3:
            buf = 'choice_' + str(j)
            choice.append(str(data.get(buf)))
            remove.append(buf)
            j += 1
        i = 0
        while i <= len(data) - 2:
            data.pop(remove[i])
            i += 1
        data['choi_content'] = '/'.join(choice)
        return super(Question, Question).\
            update("question.csv", "ques_ID", str(ques_id), data)

    @staticmethod
    def append(data):
        j = 1
        choice = []
        remove = []
        buf = ""
        while j - 1 < len(data) - 3:
            buf = "".join(['choice_',str(j)])
            choice.append(str(data.get(buf)))
            remove.append(buf)
            j += 1
        i = 0
        while i <= len(data) - 2:
            data.pop(remove[i])
            i += 1
        data['choi_content'] = '/'.join(choice)
        return super(Question, Question).\
            append("question.csv", "ques_ID", data)

    @staticmethod
    def delete(ques_id=None):
        return super(Question, Question).\
            delete("question.csv", "ques_ID", str(ques_id))


class Result(Base):

    @staticmethod
    def getkey():
        return super(Result, Result).\
            getkey("result.csv")

    @staticmethod
    def load(survey_id):
        dic = {}
        dic = super(Result, Result).\
            load("result.csv", "surv_ID", str(survey_id))
        dic['ques_ID'] = dic.get("ques_ID").split("/")
        dic['result'] = dic.get("result").split("/")
        return dic

    @staticmethod
    def update(survey_id=None):
        dl = []
        dl = Answer.load(1,None)
        buff = []
        buff = [0]*len(dl[0].get('answer').split("/"))
        temp = []
        k = 0
        for a in dl:
            temp = str(a.get('answer')).split("/")
            k = 0
            for j in temp:
                buff[k] += int(j)
                k += 1
        i = 0
        while i < len(dl[0].get('answer').split("/")):
            buff[i] = str(buff[i])
            i += 1
        dic = {}
        dic = {'result':''}
        dic['result'] = "/".join(buff)
        return super(Result, Result).\
            update("result.csv", "surv_ID", str(survey_id), **dic)

    @staticmethod
    def append(data):
        return super(Result, Result).\
            append("result.csv", "surv_ID", data)

    @staticmethod
    def delete(survey_id=None):
        Answer.delete(str(survey_id),None)
        return super(Result, Result).\
            delete("result.csv", "surv_ID", str(survey_id))


class Admin(Base):

    @staticmethod
    def getkey():
        return super(Admin, Admin).\
            getkey("admin.csv")

    @staticmethod
    def load(user_id=None):
        return super(Admin, Admin).\
            load("admin.csv", "user_ID", str(user_id))

    @staticmethod
    def update(data):
        user_id = ""
        user_id = data.get("user_ID")
        return super(Admin, Admin).\
            update("admin.csv", "user_ID", str(user_id), data)

    @staticmethod
    def append(data):
        return super(Admin, Admin).\
            append("admin.csv", "user_ID", data)

    @staticmethod
    def delete(user_id=None):
        return super(Admin, Admin).\
            delete("admin.csv", "user_ID", str(user_id))


class Res(Base):

    @staticmethod
    def getkey():
        return super(Res, Res).\
            getkey("res.csv")

    @staticmethod
    def load(user_id=None):
        return super(Res, Res).\
            load("res.csv", "user_ID", str(user_id))

    @staticmethod
    def update(data):
        user_id = ""        
        user_id = data.get("user_ID")
        return super(Res, Res).\
            update("res.csv", "user_ID", str(user_id), data)

    @staticmethod
    def append(data):
        return super(Res, Res).\
            append("res.csv", "user_ID", data)

    @staticmethod
    def delete(user_id=None):
        return super(Res, Res).\
            delete("res.csv", "user_ID", str(user_id))


class Answer(Base):

    @staticmethod
    def getkey():
        l = []
        l.extend(super(Answer, Answer).\
            getkey("answer.csv"))
        l[0] = "survey_ID"
        l.insert(0,"user_ID")
        return l

    @staticmethod
    def load(survey_id=None, user_id=None):
        if user_id == None and survey_id != None:
            answer = []
            answer = csv_read("answer.csv")
            result = []
            i = 0
            for i in answer:
               if (i.get('s/u_ID').split("/"))[0] == str(survey_id):
                    result.append(i)
            return result
        else:
            iden = ""
            iden = '/'.join([str(survey_id),str(user_id)])
            return  super(Answer, Answer).\
                load("answer.csv", "s/u_ID", iden)

    @staticmethod
    def update(data):
        survey_id = ""
        user_id = ""
        survey_id = data.get("survey_ID")
        user_id = data.get("user_ID")
        iden = ""
        iden = '/'.join([str(survey_id),str(user_id)])
        data.pop('user_ID')
        data.pop('survey_ID')
        data['s/u_ID'] = str(id)
        data['ques_ID'] = "/".join(data.get('ques_ID'))
        data['answer'] = "/".join(data.get('answer'))
        super(Answer, Answer).\
            update("answer.csv", "s/u_ID", str(iden), data)
        Result.update(str(survey_id))

    @staticmethod
    def append(data):
        survey_id = data.get("survey_ID")
        dic = {}
        dic['ques_ID'] = "/".join(data.get('ques_ID'))
        dic['answer'] = "/".join(data.get('answer'))
        dic['s/u_ID'] = "/".join([str(data.get('survey_ID')),str(data.get('user_ID'))])
        with open("./csv/"+"answer.csv", 'a') as csv_f:
            writer = DictWriter(csv_f, fieldnames=super(Answer, Answer).getkey("answer.csv"))
            writer.writerow(dic)
        Result.update(str(survey_id))


    @staticmethod
    def delete(survey_id=None, user_id = None):
        if user_id == None:
            dummy = {}
            dummy = {'s/u_ID':[],'ques_ID':[],'answer':[]}
            answer = []
            answer.extend(csv_read("answer.csv"))
            with open("./csv/"+"answer.csv", 'w') as csv_f:
                for i in answer:
                    if (i.get('s/u_ID').split("/"))[0] == str(survey_id):
                        dummy['s/u_ID'] = "-1"
                    else:
                        for j in super(Answer, Answer).getkey("answer.csv"):
                            dummy[j] = i.get(j)
                    if dummy.get('s/u_ID') != "-1":
                        writer = DictWriter(csv_f, fieldnames=super(Answer, Answer).getkey("answer.csv"))
                        writer.writerow(dummy)
        else:
            id = '/'.join([str(survey_id),str(user_id)])
            return super(Answer, Answer).\
                delete("answer.csv", "s/u_ID", id)


class Course(Base):
    @staticmethod
    def loadlist():
        li = list()
        r_li = list()
        li.extend(super(Course, Course).load("courses.csv", "course_ID", None))
        for i in li:
            r_li.append(i.get('course_ID'))
        return r_li[1:]

