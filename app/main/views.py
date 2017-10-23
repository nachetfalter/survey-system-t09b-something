'''
app/main/views.py
- - - - - - -
webpage routes for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from dateutil import parser

from flask import abort, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from . import main
from .decorators import authority_level_required
from .schedulers import Scheduler
from .validators import Validator
from ..model.models import Choice, Question, Survey, Result, Survey_Question, Answer_Record


@main.route('/')
def index():
    ''' index, temporarily redirect to login page automatically '''
    return redirect(url_for('auth.login'))


@main.route('/admin')
@login_required
@authority_level_required('Admin')
def admin_dashboard():
    ''' admin dashboard '''
    return render_template('main/admin_dashboard.html')


@main.route('/admin/questions')
@login_required
@authority_level_required('Admin')
def ad_question_pool():
    ''' admin view all questions '''
    return render_template('main/ad_question_pool.html')


@main.route('/admin/questions/create', methods=['GET', 'POST'])
@login_required
@authority_level_required('Admin')
def ad_question_create():
    ''' admin create question '''
    if request.is_json and not Validator.question_new(request.json):
        abort(400)
    elif request.is_json:
        json_data = request.json
        new_ques_id = Question.new(json_data.get('question_type'),
                                   json_data.get('question_name'))
        choices = list(zip(json_data.get('choice_content'),
                           [i+1 for i in range(len(json_data.get('choice_content')))]))
        for choice in choices:
            Choice.new(new_ques_id, choice[0], choice[1])
        return url_for('.ad_question_pool')
    return render_template('main/ad_create_question.html')


@main.route('/admin/questions/edit/<int:question_id>', methods=['GET', 'POST'])
@login_required
@authority_level_required('Admin')
def ad_question_edit(question_id):
    ''' admin edit question '''
    if request.is_json and not Validator.question_edit(request.json):
        abort(400)
    elif request.is_json:
        json_data = request.json
        Question.update(question_id,
                        json_data.get('question_type'),
                        json_data.get('question_name'))
        modi_choi_id = json_data.get('choice_id')
        modi_choi = list(zip(modi_choi_id,
                             json_data.get('choice_content'),
                             [i+1 for i in range(len(modi_choi_id))]))
        for choi_id in [choi.chID for choi in Choice.query.filter_by(qID=question_id).all()]:
            if choi_id not in modi_choi_id:
                Choice.delete(choi_id)
        for choice in modi_choi:
            if choice[0] == -1:
                Choice.new(question_id, choice[1], choice[2])
            else:
                Choice.update(choice[0], choice[1], choice[2])
        return url_for('.ad_question_pool')
    return render_template('main/ad_edit_question.html')


@main.route('/admin/questions/delete/<int:question_id>')
@login_required
@authority_level_required('Admin')
def ad_question_delete(question_id):
    ''' admin delete question '''
    if Question.load(question_id) is None:
        Question.delete(question_id)
        return url_for('.ad_question_pool')
    return jsonify({"Error": "Not Found"}), 404


@main.route('/admin/questions/view/<int:question_id>')
@login_required
@authority_level_required('Admin')
def ad_question_view(question_id):
    ''' admin preview question '''
    return render_template('main/ad_view_question.html')


@main.route('/admin/surveys')
@login_required
@authority_level_required('Admin')
def ad_survey_list():
    ''' admin view all surveys '''
    return render_template('main/ad_survey_list.html')


@main.route('/admin/surveys/create', methods=['GET', 'POST'])
@login_required
@authority_level_required('Admin')
def ad_survey_create():
    ''' admin create surveys and choose questions '''
    if request.is_json and not Validator.survey_new(request.json):
        abort(400)
    elif request.is_json:
        json_data = request.json
        new_surv_id = Survey.new(json_data.get('course_id'),
                                 json_data.get('survey_name'),
                                 parser.parse(json_data.get('start_date')),
                                 parser.parse(json_data.get('close_date')))
        ques_all = list(zip(json_data.get('question_id'),
                            [i+1 for i in range(len(json_data.get('question_id')))]))
        for ques in ques_all:
            Survey_Question.new(new_surv_id, ques[0], ques[1])
        Scheduler.add_survey_schedule_job(new_surv_id)
        return url_for('.ad_survey_list')
    return render_template('main/ad_create_survey.html')


@main.route('/admin/surveys/edit/<int:survey_id>', methods=['GET', 'POST'])
@login_required
@authority_level_required('Admin')
def ad_survey_edit(survey_id):
    ''' admin edit surveys and add or delete questions '''
    if Validator.survey_offline(survey_id):
        if request.is_json and not Validator.survey_edit(request.json):
            abort(400)
        elif request.is_json:
            json_data = request.json
            Scheduler.remove_survey_schedule_job(survey_id)
            Survey.update(survey_id,
                          json_data.get('course_id'),
                          json_data.get('survey_name'),
                          parser.parse(json_data.get('start_date')),
                          parser.parse(json_data.get('close_date')))
            ques_all = list(zip(json_data.get('survey_question_id'),
                                json_data.get('question_id'),
                                [i+1 for i in range(len(json_data.get('question_id')))]))
            old_sq = set([sq.sqID for sq in Survey_Question.query.filter_by(sID=survey_id).all()])
            del_sq = old_sq - set(json_data.get('survey_question_id'))
            for sq_id in del_sq:
                Survey_Question.delete(sq_id)
            for ques in ques_all:
                if ques[0] is None:
                    Survey_Question.new(survey_id, ques[1], ques[2])
                else:
                    Survey_Question.update(ques[0], ques[2])
            Scheduler.add_survey_schedule_job(survey_id)
            return url_for('.ad_survey_list')
        return render_template('main/ad_edit_survey.html')
    abort(403)


@main.route('/admin/surveys/delete/<int:survey_id>')
@login_required
@authority_level_required('Admin')
def ad_survey_delete(survey_id):
    ''' admin delete survey '''
    if Validator.survey_offline(survey_id):
        if Survey.load(survey_id) is None:
            Survey.delete(survey_id)
            Scheduler.remove_survey_schedule_job(survey_id)
            return url_for('.ad_survey_list')
        return jsonify({"Error": "Not Found"}), 404
    return jsonify({"Error": "Immutable"}), 400


@main.route('/admin/surveys/view/<int:survey_id>')
@login_required
@authority_level_required('Admin')
def ad_survey_view(survey_id):
    ''' admin preview survey '''
    return render_template('main/ad_view_survey.html')


@main.route('/admin/metric')
@login_required
@authority_level_required('Admin')
def ad_metric():
    ''' admin review (all) results '''
    return render_template('main/ad_metric.html')


@main.route('/admin/metric/<int:survey_id>')
@login_required
@authority_level_required('Admin')
def ad_survey_metric(survey_id):
    ''' admin review certain survey result '''
    return render_template('main/ad_survey_metric.html')


@main.route('/admin/metric/<int:survey_id>/<int:question_id>')
@login_required
@authority_level_required('Admin')
def ad_question_metric(survey_id, question_id):
    ''' admin review certain question result (in certain survey) '''
    return render_template('main/ad_question_metric.html')


@main.route('/staff')
@login_required
@authority_level_required('Staff')
def staff_dashboard():
    ''' staff dashboard '''
    return render_template('main/staff_dashboard.html')


@main.route('/staff/surveys')
@login_required
@authority_level_required('Staff')
def sf_survey_list():
    ''' staff survey list '''
    return render_template('main/sf_survey_list.html')


@main.route('/staff/surveys/edit/<int:survey_id>', methods=['GET', 'POST'])
@login_required
@authority_level_required('Staff')
def sf_survey_edit(survey_id):
    ''' staff edit survey '''
    if Validator.survey_offline(survey_id):
        if request.is_json and not Validator.survey_edit(request.json):
            abort(400)
        elif request.is_json:
            json_data = request.json
            ques_order = max([ques.order if ques.qtype == 'Gne' else 0 for ques in
                              Survey_Question.query.filter_by(sID=survey_id).all()])
            ques_all = list(zip(json_data.get('survey_question_id'),
                                json_data.get('question_id'),
                                [i+1+ques_order for i in range(len(json_data.get('question_id')))]))
            old_sq = set([sq.sqID for sq in Survey_Question.query.filter_by(sID=survey_id).all()])
            del_sq = old_sq - set(json_data.get('survey_question_id'))
            for sq_id in del_sq:
                if Survey_Question.load(sq_id).qtype == "Opt":
                    Survey_Question.delete(sq_id)
            for ques in ques_all:
                if ques[0] is None:
                    if Question.load(ques[1]).qtype == "Opt":
                        Survey_Question.new(survey_id, ques[1], ques[2])
                    else:
                        abort(400)
                else:
                    if Survey_Question.load(ques[0]).qtype == "Opt":
                        Survey_Question.update(ques[0], ques[2])
                    else:
                        abort(400)
            return url_for('.sf_survey_list')
        return render_template('main/sf_edit_survey.html')
    abort(403)


@main.route('/staff/surveys/view/<int:survey_id>')
@login_required
@authority_level_required('Staff')
def sf_survey_view(survey_id):
    ''' staff preview survey '''
    return render_template('main/sf_view_survey.html')


@main.route('/staff/metric')
@login_required
@authority_level_required('Staff')
def sf_metric():
    ''' staff review results '''
    return render_template('main/sf_metric.html')


@main.route('/staff/metric/<int:survey_id>')
@login_required
@authority_level_required('Staff')
def sf_survey_metric(survey_id):
    ''' staff review certain survey result '''
    return render_template('main/sf_survey_metric.html')


@main.route('/staff/metric/<int:survey_id>/<int:question_id>')
@login_required
@authority_level_required('Staff')
def sf_question_metric(survey_id, question_id):
    ''' staff review certain question result (in certain survey) '''
    return render_template('main/sf_question_metric.html')


@main.route('/student')
@login_required
@authority_level_required('Student')
def student_dashboard():
    ''' student dashboard '''
    return render_template('main/student_dashboard.html')


@main.route('/student/surveys')
@login_required
@authority_level_required('Student')
def st_survey_list():
    ''' student survey list '''
    return render_template('main/st_survey_list.html')


@main.route('/student/surveys/<int:surv_id>')
@login_required
@authority_level_required('Student')
def st_survey(surv_id):
    ''' redirect to first question of the survey automatically '''
    first_ques_id = Survey_Question.query.filter_by(sID=surv_id, order=1).first().sqID
    return redirect(url_for('.st_survey_questions',
                            surv_id=surv_id,
                            ques_id=first_ques_id))


@main.route('/student/surveys/<int:surv_id>/<int:surv_ques_id>', methods=['GET', 'POST'])
@login_required
@authority_level_required('Student')
def st_survey_questions(surv_id, surv_ques_id):
    ''' student do survey '''
    if request.is_json and not Validator.survey_answer(surv_id, request.json):
        abort(400)
    elif request.is_json:
        json_data = request.json
        Answer_Record.new(json_data.get('username'), surv_id)
        for i in range(len(json_data.get('question_id'))):
            Result.update_answer(json_data.get('choice_id')[i],
                                 json_data.get('answer')[i])
        return url_for('.st_thank_you')
    return render_template('main/st_do_survey.html')


@main.route('/student/metric')
@login_required
@authority_level_required('Student')
def st_metric():
    ''' student review results '''
    return render_template('main/st_metric.html')


@main.route('/student/metric/<int:survey_id>')
@login_required
@authority_level_required('Student')
def st_survey_metric(survey_id):
    ''' staff review certain survey result '''
    return render_template('main/st_survey_metric.html')


@main.route('/student/metric/<int:survey_id>/<int:question_id>')
@login_required
@authority_level_required('Student')
def st_question_metric(survey_id, question_id):
    ''' staff review certain question result (in certain survey) '''
    return render_template('main/st_question_metric.html')


@main.route('/student/surveys/thank-you')
@login_required
@authority_level_required('Student')
def st_thank_you():
    ''' show thank-you message to students '''
    return render_template('main/st_thank_you.html')
