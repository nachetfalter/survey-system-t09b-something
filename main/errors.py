'''
errors.py
- - - - - - -
custom error handler for this site
- - - - - - -
ZHENYU YAO z5125769 2017-09
'''


from flask import render_template

from . import app


# @app.errorhandler(400)
# def bad_request(e):
    # return render_template('400.html'), 400


# @app.errorhandler(401)
# def unauthorized(e):
    # return render_template('401.html'), 401


# @app.errorhandler(403)
# def forbidden(e):
    # return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# @app.errorhandler(406)
# def not_acceptable(e):
    # return render_template('406.html'), 406


@app.errorhandler(418)
def i_am_a_teapot(e):
    return render_template('418.html'), 418


# @app.errorhandler(500)
# def internal_server_error(e):
    # return render_template('500.html'), 500


# @app.errorhandler(501)
# def not_implemented(e):
    # return render_template('501.html'), 501


# @app.errorhandler(502)
# def bad_gateway(e):
    # return render_template('502.html'), 502
