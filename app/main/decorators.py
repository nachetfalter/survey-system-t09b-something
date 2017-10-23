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

# all HEAD version, i.e. JWT should be stored in request header part


def jwt_required(func):
    ''' basic JWT validation check '''
    @wraps(func)
    def wrapped(*args, **kwargs):
        ''' wrapped function, here should be a protected route (function)'''
        header = request.headers.get('Authorization', None)
        if header is None:
            abort(403)
        if header.split()[0] != "Bearer":
            abort(403)
        if not check_token(header.split()[1]):
            abort(403)
        return func(*args, **kwargs)
    return wrapped


def jwt_required_at_level(level):
    ''' extened JWT validation check, authority level is also checked here '''
    def wrapper(func):
        '''
        wrapper function, introduced to accept argument in the decorator
        '''
        @wraps(func)
        def wrapped(*args, **kwargs):
            ''' wrapped function '''
            header = request.headers.get('Authorization', None)
            if header is None:
                abort(403)
            if header.split()[0] != "Bearer":
                abort(403)
            if not get_token_user(header.split()[1]).check_auth(auth=level):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return wrapper


def authority_level_required(level):
    ''' webpage routes protection decorator '''
    def wrapper(func):
        ''' wrapper function '''
        @wraps(func)
        def wrapped(*args, **kwargs):
            ''' wrapped function '''
            if not current_user.auth == level:
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return wrapper
