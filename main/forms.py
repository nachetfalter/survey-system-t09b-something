'''
forms.py
- - - - - - -
forms for this project
- - - - - - -
ZHENYU YAO z5125769 2017-09
'''


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
     SelectField, IntegerField, TextAreaField, RadioField, BooleanField, \
     SelectMultipleField
from wtforms.validators import Required, Regexp, NumberRange, ValidationError

from .csv_io import Course, Question


class login_form(FlaskForm):
    zid = StringField(u'zID', validators=[Required(), Regexp('^zz[0-9]{7}$')])
    password = PasswordField(u'Password', validators=[Required()])
    submit = SubmitField(u'Sign in')

# temporarily unused
# def select_question_form(**kwargs):
    # ques = Question.load()
    # ques_id = list()
    # ques_name = list()
    # for q in ques:
        # ques_id.append(q.get('ques_ID'))
        # ques_name.append(q.get('quest'))
    # ques_list = list(zip(ques_id, ques_name))
    # class smul_f(FlaskForm):
        # question_list = SelectMultipleField(u'Question List', choices=ques_list)
    # return smul_f(**kwargs)


# TODO raise ValidationError
class create_survey_form(FlaskForm):
    ques = Question.load()
    ques_id = list()
    ques_name = list()
    for q in ques:
        ques_id.append(q.get('ques_ID'))
        ques_name.append(q.get('quest'))
    cour_list = Course.loadlist()
    def validate(self):
        if self.cancel_.data:
            return True
        else:
            if self.survey_name.data and self.course_code.data and \
                self.question_list.data:
                return True
            return False
    survey_name = StringField(u'Survey Name')
    course_code = SelectField(u'Course Code',
        choices=list(zip(cour_list, cour_list)))
    question_list = SelectMultipleField(u'Question List',
                                        choices=list(zip(ques_id, ques_name)))
    cancel_ = SubmitField(u'Cancel')
    create_ = SubmitField(u'Create')


# TODO raise ValidationError
class choose_question_type_form(FlaskForm):
    def validate(self):
        if self.cancel_.data:
            return True
        else:
            if not self.question_name.data and self.choice_number.data:
                return False
            return True
    question_name = StringField(u'Question Name')
    # NOTE temporarily unused
    # question_type = SelectField(u'Qusetion type',
        # choices=[('mco', "Multiple Choice"), ('sa', "Short Answer"),
        # ('mcm', "Multiple Choice with Several Answers")])
    choice_number = IntegerField(u'Choices Number',
        validators=[NumberRange(min=2, max=8)])
    cancel_ = SubmitField(u'Cancel')
    next_ = SubmitField(u'Next')


# TODO raise ValidationError
# mc for Multiple Choice
# generate form with dynamic number of StringFields for creating questions
def create_question_mc_form(number, **kwargs):
    class str_f(FlaskForm):
        def validate(self):
            if self.back_.data:
                return True
            else:
                name_list = ['choice_{0}'.format(n)
                             for n in range(1, int(number)+1)]
                for name in name_list:
                    if not getattr(getattr(self, name), 'data'):
                        return False
                return True
    name_list = ['choice_{0}'.format(n) for n in range(1, int(number)+1)]
    for name in name_list:
        setattr(str_f, name, StringField(name.replace('_', ' ').capitalize()))
    setattr(str_f, 'back_', SubmitField(u'Back'))
    setattr(str_f, 'create_', SubmitField(u'Create'))
    return str_f(**kwargs)


# sa for Short Answer
# nothing to do actually
class create_question_sa_form(FlaskForm):
    pass


# FIXME validation problem of radio field to be fixed
# TODO raise ValidationError
# mco for Multiple Choice with One Answer
# generate form with dynamic number of RadioFields for answering questions
# validate should be re-organized in views.py
def create_answer_mco_form(name, choices, **kwargs):
    class rad_f(FlaskForm):
        radio_f = RadioField(name)  # can be extended
        back_ = SubmitField(u'Back')
        next_ = SubmitField(u'Next')
        def validate(self):
            if self.back_.data:
                return True
            elif self.radio_f.data is not None:
                return True
            else:
                return False
    form = rad_f(**kwargs)
    form.radio_f.choices = list(zip([c for c in range(len(choices))], choices))
    return form


# TODO raise ValidationError
# mcm for Multiple Choice with Multiple Answer
# generate form with dynamic number of BooleanFields for answering questions
# validate should be re-organized in views.py
def create_answer_mcm_form(name, choices, **kwargs):
    class boo_f(FlaskForm):
        def validate(self):
            if self.back_.data:
                return True
            else:
                i = 0
                for choice in choices:
                    if not getattr(getattr(self, choice), 'data'):
                        i += 1
                return i
    for choice in choices:
        setattr(boo_f, choice, BooleanField(choice))
    setattr(boo_f, 'back_', SubmitField(u'Back'))
    setattr(boo_f, 'next_', SubmitField(u'Next'))
    return boo_f(**kwargs)


# FIXME to be rewritten
# temporarily unused
# sa for Short Answer
# generate form with a TextAreaField
# class create_answer_sa_form(FlaskForm):
    # answer = TextAreaField(u"Answer", validators=[Required()])
    # submit = SubmitField(u'Next')


# TODO todo list
# forms creating admins and/or users
# forms importing course details
# forms sending emails
