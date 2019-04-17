from flask import Blueprint, g, current_app, request
from ..utils import log

mod = Blueprint('hook', __name__)


@mod.before_app_first_request
def before_first_req():
    pass


@mod.before_app_request
def before_req():
    ip, host, scheme = get_remote_info()
    # connect database
    redis = current_app.config['REDIS']
    g.redis = redis.connect()
    # confirm cors to set response's headers
    if host in current_app.config.get("ALLOWED_HOST", []):
        g.CORS_valid = True
    else:
        g.CORS_valid = False


@mod.after_app_request
def after_req(response):
    """might not be executed at the end of the request
    in case of an unhandled exception occurred.
    """
    try:
        ip, host, scheme = get_remote_info()
        if g.CORS_valid:
            # CORS
            response.headers['Access-Control-Allow-Origin'] = '{}://{}'.format(scheme, host)
            response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER,Content-Type'
            response.headers['Access-Control-Max-Age'] = '86400'
        # log when need
        if current_app.config.get('ENABLE_CUSTOMIZED_LOG', False):
            http_method = request.method
            path = request.environ.get('REQUEST_URI', request.path)
            code = response.status_code
            log_info = "{} [{} {}] {}".format(ip, http_method, path, code)
            # current_app.logger.info(log_info)
            log(log_info, target='my-request.log', isprint=True)
    finally:
        return response


def get_remote_info():
    """
    :return ip, host, scheme
    """
    if current_app.config.get("REVERSE_PROXY", "").lower() == 'nginx':
        return str(request.headers.get('X-Real-IP')), \
               str(request.headers.get('Host')), \
               str(request.headers.get('X-Real-Scheme'))
    return request.remote_addr, request.host, request.scheme


def analysis_referer(referer: str):
    try:
        # 简单校验
        if not referer or len(referer) < 3:
            return '', 0
        # 去除协议头
        referer = referer.strip('/')
        if referer.startswith('https://'):
            referer = referer[8:]
        elif referer.startswith('http://'):
            referer = referer[7:]
        # 去除路径
        if '/' in referer:
            t = referer.split('/', 1)
            referer = t[0]
        # 获得host, port
        if ':' in referer:
            r = referer.split(':')
            if len(r) == 2 and r[1].isdigit():
                return r[0], int(r[1])
            else:
                return '', 0
        return referer, 80

    except Exception as e:
        print('analysis referer error: ', repr(e))
        return '', 0

