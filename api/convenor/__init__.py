__all__ = []
from flask import render_template, session, Blueprint, request
from datetime import date
import pkgutil
import inspect

ALLOWED_EXTENSIONS = set(['csv'])
convenor_blueprint = Blueprint("convenor", __name__, url_prefix="/convenor")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def normalize_model(models: list[dict]) -> list[dict]:
    """Normalize a model replace None with empty string"""
    for index in range(len(models)):
        model = models[index]
        for key, value in model.items():
            if value is None:
                model[key] = ''
    return models


def is_empty(value) -> bool:
    """Check if given value is None or empty string."""
    return value is None or value == ""


def normalize_field(value):
    """Returns a normalize input field"""
    return None if value == "" else value


def get_int(value: str | None) -> int | None:
    """Get int of value"""
    return None if value is None or value == '' else int(value)


@convenor_blueprint.route("error", methods=["POST", "GET", "DELETE"])
def error_page():
    error_message = session.pop('error')
    return render_template("convenor/error.html", error_message=error_message)


@convenor_blueprint.app_context_processor
def inject_year():
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
