'''
app/auth/errors.py
- - - - - - -
custom error handler for package 'auth' in VM
- - - - - - -
ZHENYU YAO z5125769 2017-10
'''


from flask import jsonify, render_template, request

from . import auth


@auth.errorhandler(400)
def bad_request(e):
    if request.is_json or not request.accept_mimetypes.accept_html:
        return jsonify({"Error": "Bad Request"}), 400
    return render_template('400.html'), 400


@auth.errorhandler(403)
def forbidden(e):
    if request.is_json or not request.accept_mimetypes.accept_html:
        return jsonify({"Error": "Forbidden"}), 403
    return render_template('403.html'), 403


@auth.errorhandler(404)
def not_found(e):
    if request.is_json or not request.accept_mimetypes.accept_html:
        return jsonify({"Error": "Not Found"}), 404
    return render_template('404.html'), 404


@auth.errorhandler(418)
def i_am_a_teapot(e):
    return render_template('418.html'), 418
