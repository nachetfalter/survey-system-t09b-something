'''
app/auth/api.py
- - - - - - -
api routes for package 'auth' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from datetime import datetime, timedelta
from flask import abort, current_app, jsonify, request

import jwt

from . import auth
from ..model.models import User


@auth.route('/api/auth/gen', methods=['POST'])
def gen_token():
    '''
    generate auth token, with one day validation time
    '''
    if request.is_json:
        json_data = request.json
        username = json_data.get('username')
        user = User.query.filter_by(zID=username).first()
        if user and user.verify_password(json_data.get('password')):
            payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=0),
                'iat': datetime.now(),
                'identity': username
            }
            return jsonify({
                "token": jwt.encode(
                    payload,
                    current_app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                ).decode('utf-8')
            }), 200
    return jsonify({'Error': 'Not This Identity'}), 400


def check_token(token):
    '''
    check token validation
    detailed error message ommitted here
    '''
    try:
        jwt.decode(token, current_app.config.get('SECRET_KEY'))
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'error': 'bad request'}), 400
    return True


def get_token_user(token):
    '''
    get token identity, whole version of the function "check_token"
    detailed error message ommitted here as well
    '''
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'error': 'bad request'}), 400
    user = User.query.filter_by(zID=payload['identity']).first()
    if user is None:
        abort(403)
    return user
