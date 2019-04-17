import os
from .redis_operation import MyRedis

basedir = os.path.abspath(os.path.dirname(__file__))

enable_customized_log = os.environ.get('ENABLE_CUSTOMIZED_LOG', default=True)
enable_customized_log = False if enable_customized_log == '0' else True


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', default='a difficult key for flask')
    ALLOWED_HOST = ('xchens.cn', '127.0.0.1')
    MAX_DATA_EXPIRE_TIME = 60*60*24*3  # 3 days
    PASTE_PUBLIC_KEY_PREFIX = b'PASTE_PUBLIC_'
    PASTE_SECRET_KEY_PREFIX = b'PASTE_SECRET_'
    ENABLE_CUSTOMIZED_LOG = enable_customized_log  # my log
    JSON_AS_ASCII = False  # jsonify response support chinese
    REVERSE_PROXY = ""  # 反向代理


class DevelopmentConfig(BaseConfig):
    REDIS = MyRedis()


class ProductionConfig(BaseConfig):
    pass



