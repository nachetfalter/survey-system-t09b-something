'''
app/main/api.py
- - - - - - -
api routes for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import jsonify, request, url_for

from . import main
from .decorators import jwt_required, jwt_required_at_level
from ..auth.api import get_token_user
from ..model.models import User, Course, Question, Survey, Result, Survey_Question


# FIXME minor data visible problem to be fixed


@main.route('/api/user/<string:user_id>')
@jwt_required
def user_api(user_id):
    ''' fetch user info, privacy protection enabled '''
    token = request.headers.get('Authorization').split()[1]
    user = User.load(user_id)
    if user is not None:
        if get_token_user(token).zID == user_id or \
                get_token_user(token).auth == 'Admin':
            user_dict = user.extract()
            user_dict.pop('_password')
            return jsonify(user_dict), 200
        return jsonify({'Error': 'Not Permitted'}), 403
    return jsonify({"Error": "Not Found"}), 404


@main.route('/api/course/')
@jwt_required_at_level('Staff')
def course_list_api():
    ''' fetch course list '''
    c_all = Course.load()
    return jsonify({"courses": [course.extract() for course in c_all]}), 200


@main.route('/api/question/')
@jwt_required_at_level('Admin')
def question_pool_all_api():
    ''' fetch question pool info '''
    ques_all = Question.load()
    ques_all = [ques.extract() for ques in ques_all]
    for ques in ques_all:
        ques.pop('chID')
        ques.pop('cho_con')
    return jsonify({'questions': ques_all}), 200


@main.route('/api/question/<int:question_id>')
@jwt_required_at_level('Admin')
def question_pool_api(question_id):
    ''' fetch question details in question pool '''
    ques = Question.load(question_id)
    if ques is not None:
        return jsonify(ques.extract()), 200
    return jsonify({"Error": "Not Found"}), 404


@main.route('/api/survey_operation/<int:survey_id>')
@jwt_required_at_level('Staff')
def survey_operation_api(survey_id):
    ''' change survey status '''
    surv = Survey.load(survey_id)
    if surv is not None:
        new_status = Survey.status_operation(survey_id)
        return jsonify({"status": new_status}), 200
    return jsonify({"Error": "Not Found"}), 404


@main.route('/api/survey/')
@jwt_required_at_level('Admin')
def survey_all_api():
    ''' fetch survey list info '''
    surv_all = Survey.load()
    return jsonify({'surveys': [surv.extract() for surv in surv_all]}), 200


@main.route('/api/survey/<int:survey_id>')
@jwt_required
def survey_api(survey_id):
    ''' fetch survey details in survey list '''
    surv = Survey.load(survey_id)
    if surv is not None:
        return jsonify(surv.extract()), 200
    return jsonify({"Error": "Not Found"}), 404


@main.route('/api/survey_question/<int:question_id>')
@jwt_required
def survey_question_api(question_id):
    ''' fetch survey_question details in survey-doing page '''
    ques = Survey_Question.load(question_id)
    if ques is not None:
        return jsonify(ques.extract()), 200
    return jsonify({"Error": "Not Found"}), 404


@main.route('/api/survey_specified_question/<int:survey_id>')
@jwt_required_at_level('Staff')
def survey_specified_questions_api(survey_id):
    ''' fetch survey-specified question pool '''
    surv = Survey.load(survey_id)
    if surv is None:
        return jsonify({"Error": "Not Found"}), 404
    ques_all = list()
    for ques in Question.load():
        if ques.qID not in surv.extract().get('sqID'):
            setattr(ques, 'sqID', None)
            ques_all.append(ques)
    for sq_id in surv.extract().get('sqID'):
        sq_ins = Survey_Question.load(sq_id)
        ques_all.append(sq_ins)
    return jsonify({'survey_specified_questions':
                    [ques.extract() for ques in ques_all]}), 200


@main.route('/api/result/question/<int:question_id>')
@jwt_required
def question_result_api(question_id):
    ''' fetch result by (survey) question id '''
    ques = Survey_Question.load(question_id)
    if ques is None:
        return jsonify({"Error": "Not Found"}), 404
    ques_dict = ques.extract()
    choi_all = list()
    for choi_id in ques_dict.get('chID'):
        choi = Result.load(choi_id).extract()
        choi_all.append(choi)
    ques_dict.pop('chID')
    ques_dict['results'] = choi_all
    return jsonify(ques_dict), 200


@main.route('/api/result/survey/<int:survey_id>')
@jwt_required
def survey_result_api(survey_id):
    ''' fetch result by survey id '''
    surv = Survey.load(survey_id)
    if surv is None:
        return jsonify({"Error": "Not Found"}), 404
    surv_dict = surv.extract()
    ques_all_url = list()
    for ques_id in surv_dict.get('sqID'):
        ques = url_for('.question_result_api', question_id=ques_id, _external=True)
        ques_all_url.append(ques)
    return jsonify({'results_url': ques_all_url}), 200
