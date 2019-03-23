from flask import Blueprint, jsonify, current_app, request


mod = Blueprint('paste', __name__, url_prefix='/api/paste')


@mod.route('/read/', defaults={'content_id': 0})
@mod.route('/read/<int:content_id>')
def read(content_id: int):

    return jsonify({'content_id': content_id})











