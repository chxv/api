import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', default='a difficult key for flask')
    DATABASE_URI = ''


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass



