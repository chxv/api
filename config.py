import os
from .redis_operation import MyRedis

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', default='a difficult key for flask')
    ALLOWED_ORIGIN = ('xchens.cn', '127.0.0.1')


class DevelopmentConfig(BaseConfig):
    REDIS = MyRedis()


class ProductionConfig(BaseConfig):
    pass



