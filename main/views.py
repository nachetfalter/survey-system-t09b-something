'''
views.py
- - - - - - -
routes for this site
- - - - - - -
ZHENYU YAO z5125769 2017-09
'''


from flask import redirect, url_for, render_template, session, request
from flask import abort  # , flash
# TODO to be introduced in next stage
# from flask_login import login_required, login_user, logout_user

from . import app
from . import forms
from . import csv_io as data_io


# index, temporarily redirect to login page automatically
@app.route('/')
def index():
    return redirect('login')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.login_form()
    if form.validate_on_submit() and \
            form.zid.data == 'z2333333' and form.password.data == 'password':
        return redirect(url_for('admin'))
    return render_template("login.html", form=form)


# admin control panel
@app.route('/admin')
# TODO use flask-login
# @login_required
def admin():
    return render_template('admin_panel.html')


# view all questions
@app.route('/admin/questions')
# TODO use flask-login
# @login_required
def ad_question_pool():
    ques_pool = data_io.Question.load()
    session.pop('num', None)
    return render_template('question_pool.html', ques_pool=ques_pool)


# create question
@app.route('/admin/questions/create', methods=['GET', 'POST'])
# TODO use flask-login
# @login_required
def ad_question_create():
    if 'num' not in session.keys():
        form = forms.choose_question_type_form()
        # TODO need to catch exception here
        # try:
        # except ValidationError:
        # finally:
        if form.validate_on_submit():
            if form.cancel_.data:
                return redirect(url_for('ad_question_pool'))
            else:
                session['num'] = form.choice_number.data
                session['ques_name'] = form.question_name.data
                return redirect(url_for('ad_question_create'))
    else:
        form = forms.create_question_mc_form(session['num'])
        # TODO need to catch exception here
        # try:
        # except ValidationError:
        # finally:
        if form.validate_on_submit():
            if form.back_.data:
                session.pop('num')
                return redirect(url_for('ad_question_create'))
            else:
                key = data_io.Question.getkey(session['num'])
                value = [int(), session['ques_name'], session['num']]
                fields = ['choice_{0}'.format(n)
                          for n in range(1, int(session['num'])+1)]
                for name in fields:
                    value.append(str(getattr(getattr(form, name), 'data')))
                new_ques = dict(zip(key, value))
                data_io.Question.append(new_ques)
                return redirect(url_for('ad_question_pool'))
    return render_template('create_question.html', form=form)


# TODO to be refactored with flask-cache
@app.route('/admin/questions/edit', methods=['GET', 'POST'])
# TODO use flask-login
# @login_required
def ad_question_edit():
    ques_id = request.values.get('question_id', None)
    if ques_id is not None:
        session['ques_id'] = int(ques_id)
    ques = data_io.Question.load(session['ques_id'])
    ques_name = request.args.get('ques_name') or ques.get('quest')
    choi_num = request.args.get('choi_num') or int(ques.get('choi_num'))
    step = request.args.get('step', 1)
    if step == 1:
        form = forms.choose_question_type_form()
        # TODO need to catch exception here
        # try:
        # except ValidationError:
        # finally:
        if form.cancel_.data and form.validate_on_submit():
            return redirect(url_for('ad_question_pool'))
        if form.next_.data and form.validate_on_submit():
            return redirect(url_for('ad_question_edit',
                                    question_id=session['ques_id'],
                                    ques_name=form.question_name.data,
                                    choi_num=form.choice_number.data, step=2))
        form.question_name.data = ques_name
        form.choice_number.data = choi_num
        return render_template('edit_question.html', form=form)
    else:
        choi_num = int(choi_num)
        form = forms.create_question_mc_form(choi_num)
        # TODO need to catch exception here
        # try:
        # except ValidationError:
        # finally:
        if form.back_.data and form.validate_on_submit():
            return redirect(url_for('ad_question_edit',
                                    question_id=session['ques_id'],
                                    ques_name=ques_name,
                                    choi_num=choi_num))
        if form.create_.data and form.validate_on_submit():
            key = data_io.Question.getkey(choi_num)
            value = [ques['ques_ID'], ques_name, choi_num]
            fields = ['choice_{0}'.format(n)
                      for n in range(1, choi_num+1)]
            for name in fields:
                value.append(str(getattr(getattr(form, name), 'data')))
            value = [str(v) for v in value]
            modi_ques = dict(zip(key, value))
            data_io.Question.update(modi_ques)
            return redirect(url_for('ad_question_pool'))
        choi = dict(ques)
        choi.pop('choi_num')
        choi.pop('ques_ID')
        choi.pop('quest')
        for key, value in choi.items():
            try:
                setattr(getattr(form, key), 'data', value)
            except:
                pass
        return render_template('edit_question.html', form=form)


# delete question
@app.route('/admin/questions/delete', methods=['POST'])
# TODO use flask-login
# @login_required
def ad_question_delete():
    data_io.Question.delete(request.form.get('question_id'))
    return redirect(url_for('ad_question_pool'))


# preview question
@app.route('/admin/questions/view', methods=['POST'])
# TODO under construction
# @login_required
def ad_question_view():
    ques = data_io.Question.load(request.form.get('question_id'))
    ques_choi_name = ['choice_{0}'.format(n)
                      for n in range(1, int(ques.get('choi_num'))+1)]
    ques_choi = list()
    for name in ques_choi_name:
        ques_choi.append(ques.get(name))
        ques.pop(name)
    ques.update({'choi_content': ques_choi})
    return render_template('view_question.html', ques=ques)


# view all surveys
@app.route('/admin/surveys')
# TODO use flask-login
# @login_required
def ad_survey_list():
    surv_list = data_io.Survey.load()
    return render_template('survey_list.html', surv_list=surv_list)


# create surveys and choose questions
@app.route('/admin/surveys/create', methods=['GET', 'POST'])
# TODO use flask-login
# @login_required
def ad_survey_create():
    ques_list = data_io.Question.load()
    ques_id = list()
    ques_name = list()
    for ques in ques_list:
        ques_id.append(ques.get('ques_ID'))
        ques_name.append(ques.get('quest'))
    choices = list(zip(ques_id, ques_name))
    form = forms.create_survey_form(choices)
    # TODO need to catch exception here
    # try:
    # except ValidationError:
    # finally:
    if form.validate_on_submit():
        if not form.cancel_.data:
            key = data_io.Survey.getkey()
            value = [int(), form.course_code.data, form.question_list.data,
                     form.survey_name.data]
            new_surv = dict(zip(key, value))
            data_io.Survey.append(new_surv)
        return redirect(url_for('ad_survey_list'))
    return render_template('create_survey.html', form=form)


# TODO selectfield population, js may needed
# edit surveys and choose questions
@app.route('/admin/surveys/edit', methods=['POST'])
# TODO use flask-login
# @login_required
def ad_survey_edit():
    surv_id = request.values.get('survey_id')
    if surv_id is not None:
        surv_id = int(surv_id)
        session['surv_id'] = surv_id
    else:
        surv_id = session['surv_id']
    surv = data_io.Survey.load(surv_id)
    ques_list = data_io.Question.load()
    ques_id = list()
    ques_name = list()
    for ques in ques_list:
        ques_id.append(ques.get('ques_ID'))
        ques_name.append(ques.get('quest'))
    choices = list(zip(ques_id, ques_name))
    form = forms.create_survey_form(choices)
    # TODO need to catch exception here
    # try:
    # except ValidationError:
    # finally:
    if form.create_.data and form.validate_on_submit():
        key = data_io.Survey.getkey()
        value = [surv_id, form.course_code.data, form.question_list.data,
                 form.survey_name.data]
        modi_surv = dict(zip(key, value))
        data_io.Survey.update(modi_surv)
        return redirect(url_for('ad_survey_list'))
    if form.cancel_.data and form.validate_on_submit():
        return redirect(url_for('ad_survey_list'))
    form.survey_name.data = surv.get('surv_name')
    form.course_code.process_data(surv.get('course_ID'))
    form.question_list.process_data(surv.get('ques_ID'))
    return render_template('edit_survey.html', form=form)


# delete survey
@app.route('/admin/surveys/delete', methods=['POST'])
# TODO use flask-login
# @login_required
def ad_survey_delete():
    data_io.Survey.delete(request.form.get('survey_id'))
    return redirect(url_for('ad_survey_list'))


# preview survey
@app.route('/admin/surveys/view', methods=['POST'])
# TODO use flask-login
# @login_required
def ad_survey_view():
    surv = data_io.Survey.load(request.form.get('survey_id'))
    ques_id_list = [int(i) for i in surv.get('ques_ID')]
    ques_list = list()
    for ques_id in ques_id_list:
        ques_list.append(data_io.Question.load(ques_id))
    return render_template('view_survey.html', surv=surv, ques_list=ques_list)


# TODO to be implemented in next stage
# collect survey result
@app.route('/admin/surveys/result', methods=['POST'])
# TODO use flask-login
# @login_required
def ad_survey_result():
    abort(418)


# result root access forbidden
@app.route('/result')
def result():
    abort(403)


# TODO to be implemented in next stage
# display result
@app.route('/result/<surv_id>')
def result_surv(surv_id):
    surv = data_io.Survey.load(surv_id)
    ques_id_list = [int(i) for i in surv.get('ques_ID')]
    ques_list = list()
    for ques_id in ques_id_list:
        ques_list.append(data_io.Question.load(ques_id))
    resu = data_io.Result.load(surv_id)
    return render_template("result.html", surv=surv, ques_list=ques_list,
                           resu=resu)


# XXX abandoned
@app.route('/survey')
def us_survey_list():
    abort(403)


# redirect to first question of the survey automatically
@app.route('/survey/<surv_id>')
def us_survey(surv_id):
    session.pop('answer', None)
    data = data_io.Survey.load(int(surv_id)).get('ques_ID')
    return redirect(url_for('us_survey_questions', surv_id=surv_id,
                            ques_id=data[0]))


# FIXME validation problem to be fixed
# TODO to be refactored with flask-cache
# (respondents) do survey at this route
@app.route('/survey/<surv_id>/<ques_id>', methods=['GET', 'POST'])
def us_survey_questions(surv_id, ques_id):
    if 'answer' not in session.keys():
        session['answer'] = int()
    answ = session['answer']
    surv = data_io.Survey.load(surv_id)
    ques = data_io.Question.load(ques_id)
    choices = list()
    for i in range(1, int(ques.get('choi_num'))+1):
        choi_name = "choice_"+str(i)
        choices.append(ques.get(choi_name))
    form = forms.create_answer_mco_form(ques.get('quest'), choices)
    ques_id_list = surv.get('ques_ID')
    ques_index = ques_id_list.index(ques_id)
    if ques_index < len(ques_id_list) - 1:
        next_ques_id = ques_id_list[ques_index+1]
    else:
        next_ques_id = "TEM"
    if ques_index > 0:
        prev_ques_id = ques_id_list[ques_index-1]
    else:
        prev_ques_id = "STA"
    # TODO need to catch exception here
    # try:
    # except ValidationError:
    # finally:
    if form.validate_on_submit():
        answ = answ * 10
        try:
            answ = answ + int(form.radio_f.data) + 1
        except ValueError:
            pass
        session['answer'] = answ
        if form.back_.data and prev_ques_id != "STA":
            return redirect(url_for('us_survey_questions',
                                    surv_id=surv_id, ques_id=prev_ques_id))
        elif form.back_.data:
            session.pop('ques_id', None)
            session.pop('answer', None)
            # TODO logic to be modified
            return redirect(url_for('us_survey', surv_id=surv_id))
        elif form.next_.data and next_ques_id != "TEM":
            return redirect(url_for('us_survey_questions',
                                    surv_id=surv_id, ques_id=next_ques_id))
        else:
            key = data_io.Answer.getkey()
            answ_list = [str(int(a)-1) for a in str(session['answer'])]
            while len(answ_list) < len(ques_id_list):
                answ_list.insert(0, '0')
            # TODO identify user here
            value = [int(), surv_id, ques_id_list, answ_list]
            data = dict(zip(key, value))
            data_io.Answer.append(data)
            return redirect(url_for('thank_you'))
    return render_template('do_survey.html', ques_name=ques.get('quest'),
                           form=form)


# show thank-you message to respondents
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


# NOTE test use only, modify before using
@app.route('/test_success')
def test_success():
    abort(418)
    return "<h3>Success.</h3>"
