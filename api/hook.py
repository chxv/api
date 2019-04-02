from flask import Blueprint, g, current_app

mod = Blueprint('hook', __name__)


@mod.before_app_first_request
def before_first_req():
    pass


@mod.before_app_request
def before_req():
    redis = current_app.config['REDIS']
    g.redis = redis.connect()


@mod.after_app_request
def after_req(response):
    """might not be executed at the end of the request
    in case of an unhandled exception occurred.
    """
    return response






