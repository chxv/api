import os
from .redis_operation import MyRedis

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', default='a difficult key for flask')
    ALLOWED_ORIGIN = ('xchens.cn', '127.0.0.1')
    MAX_DATA_EXPIRE_TIME = 60*60*24*3  # 3 days
    PASTE_PUBLIC_KEY_PREFIX = b'PASTE_PUBLIC_'
    PASTE_SECRET_KEY_PREFIX = b'PASTE_SECRET_'
    ENABLE_CUSTOMIZED_LOG = os.environ.get('ENABLE_CUSTOMIZED_LOG', default=True)  # my log


class DevelopmentConfig(BaseConfig):
    REDIS = MyRedis()


class ProductionConfig(BaseConfig):
    pass



