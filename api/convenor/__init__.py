__all__ = []
from flask import \
    redirect, render_template, send_from_directory, session, url_for,\
    Blueprint, request
from datetime import date
from api import app
from api.cached_items import get_upcoming_games, get_leagues
from api.authentication import get_user_information
import pkgutil
import inspect


convenor_blueprint = Blueprint("convenor", __name__, url_prefix="/convenor")


@convenor_blueprint.route("error")
def error_page():
    error_message = session.pop('error')
    return render_template("convenor/error.html", error_message=error_message)


@convenor_blueprint.app_context_processor
def inject_htmx():
    return dict(year=date.today().year)


@convenor_blueprint.app_context_processor
def inject_htmx():
    return dict(snippet=request.headers.get("Hx-Request", False))

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)