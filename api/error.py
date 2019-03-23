from flask import Blueprint, jsonify

mod = Blueprint('error', __name__, url_prefix='/error')


@mod.app_errorhandler(403)
def forbidden(e):
    """Forbidden"""
    return jsonify({'common': {'code': 403, 'msg': '403 Forbidden'}}), 403


@mod.app_errorhandler(404)
def page_not_found(e):
    """Not Found"""
    return jsonify({'common': {'code': 404, 'msg': '404 Not Found'}}), 404


@mod.app_errorhandler(405)
def method_not_allowed(e):
    """Method not allowed"""
    return jsonify({'common': {'code': 405, 'msg': '405 Method Not Allowed'}}), 405


@mod.app_errorhandler(500)
def internal_server_error(e):
    """Internal server error"""
    return jsonify({'common': {'code': 500, 'msg': '500 Internal Server Error'}}), 500



