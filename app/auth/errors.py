'''
app/auth/errors.py
- - - - - - -
custom error handler for package 'auth' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


# TODO to be rewritten


from flask import jsonify, render_template, request

from . import auth


@auth.errorhandler(400)
def bad_request(e):
    if request.is_json or not request.accept_mimetypes.accept_html:
        return jsonify({"Error": "Bad Token"}), 400
    return "Bad Token", 400


@auth.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


# @auth.errorhandler(403)
# def forbidden(e):
    # return render_template('403.html'), 403


@auth.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# @auth.errorhandler(406)
# def not_acceptable(e):
    # return render_template('406.html'), 406


@auth.errorhandler(418)
def i_am_a_teapot(e):
    return render_template('418.html'), 418


# @auth.errorhandler(500)
# def internal_server_error(e):
    # return render_template('500.html'), 500


# @auth.errorhandler(501)
# def not_implemented(e):
    # return render_template('501.html'), 501


# @auth.errorhandler(502)
# def bad_gateway(e):
    # return render_template('502.html'), 502
