'''
app/main/decorators.py
- - - - - - -
custom decorators for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from functools import wraps
from flask import abort, request
from flask_login import current_user

from ..auth.api import check_token, get_token_user


# JSON ver
# def jwt_required(f):
    # @wraps(f)
    # def wrapped(*args, **kwargs):
        # if not request.is_json or request.json.get('token', None) is None:
            # abort(403)
        # if not check_token(request.json.get('token')):
            # abort(403)
        # return f(*args, **kwargs)
    # return wrapped


# HEAD ver
def jwt_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        header = request.headers.get('Authorization', None)
        if header is None:
            abort(403)
        if header.split()[0] != "Bearer":
            abort(403)
        if not check_token(header.split()[1]):
            abort(403)
        return f(*args, **kwargs)
    return wrapped


# HEAD ver as well
def jwt_required_at_level(level):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            header = request.headers.get('Authorization', None)
            if header is None:
                abort(403)
            if header.split()[0] != "Bearer":
                abort(403)
            if not get_token_user(header.split()[1]).check_auth(auth=level):
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# protect webpage routes
def authority_level_required(level):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.auth == level:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
