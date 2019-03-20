from flask import Blueprint, g

mod = Blueprint('hook', __name__)


@mod.before_app_first_request
def before_first_req():
    g


@mod.before_app_request
def before_req():
    g


@mod.after_app_request
def after_req(response):
    """might not be executed at the end of the request in case an unhandled exception occurred."""
    return response






