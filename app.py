from flask import Flask, jsonify, current_app, url_for
from .config import DevelopmentConfig, ProductionConfig
from . import *  # mod


def register_mod(app_: Flask) -> None:
    """将所有路由蓝本进行注册"""
    app_.register_blueprint(error_mod)
    app_.register_blueprint(hook_mod)


def create_app(config) -> Flask:
    app_ = Flask(__name__)           # create app
    app_.config.from_object(config)  # update config
    register_mod(app_)               # 注册路由蓝本
    return app_


app = create_app(DevelopmentConfig)



