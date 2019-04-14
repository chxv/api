from flask import Blueprint, g, current_app, request
from ..utils import log

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
    try:
        # log when need
        if current_app.config.get('ENABLE_CUSTOMIZED_LOG', False):
            ip, protocol = get_remote_info()
            http_method = request.method
            path = request.environ.get('REQUEST_URI', request.path)
            code = response.status_code
            log_info = "{} [{} {}] {} {}".format(ip, http_method, path, protocol, code)
            # current_app.logger.info(log_info)
            log(log_info, target='my-request.log', isprint=True)
    finally:
        return response


def get_remote_info():
    """ip protocol"""
    return request.remote_addr, request.environ.get('SERVER_PROTOCOL')




