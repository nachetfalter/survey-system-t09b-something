'''
app/main/errors.py
- - - - - - -
custom error handler for package 'main' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import render_template

from . import main


# TODO to be rewritten

# @main.errorhandler(400)
# def bad_request(e):
    # return render_template('400.html'), 400


# @main.errorhandler(401)
# def unauthorized(e):
    # return render_template('401.html'), 401


@main.errorhandler(403)
def forbidden(e):
    # return render_template('403.html'), 403
    return '403', 403


@main.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# @main.errorhandler(406)
# def not_acceptable(e):
    # return render_template('406.html'), 406


@main.errorhandler(418)
def i_am_a_teapot(e):
    return render_template('418.html'), 418


# @main.errorhandler(500)
# def internal_server_error(e):
    # return render_template('500.html'), 500


# @main.errorhandler(501)
# def not_implemented(e):
    # return render_template('501.html'), 501


# @main.errorhandler(502)
# def bad_gateway(e):
    # return render_template('502.html'), 502
