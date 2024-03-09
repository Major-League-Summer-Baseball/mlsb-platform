# -*- coding: utf-8 -*-
"""
    The main entry into the website.

    Contains the index page and other things for crawlers/facebook
"""
__all__ = []
from flask import \
    redirect, render_template, send_from_directory, url_for, Blueprint, request
from datetime import date
from api import app
from api.cached_items import get_website_base_data as base_data
from api.cached_items import get_upcoming_games
from api.authentication import get_user_information
import pkgutil
import inspect

website_blueprint = Blueprint("website", __name__, url_prefix="/")


@website_blueprint.app_context_processor
def inject_htmx():
    return dict(snippet=request.headers.get("Hx-Request", False))


@website_blueprint.route("/")
@website_blueprint.route("/website")
@website_blueprint.route("/website/")
def reroute():
    year = date.today().year
    return redirect(url_for("website.index", year=year))


@website_blueprint.route("/about")
def general_about():
    year = date.today().year
    return redirect(url_for("website.about", year=year))


@website_blueprint.route("/about/<int:year>")
def about(year):
    return render_template(
        "website/about.html",
        base=base_data(year),
        title="About",
        year=year,
        games=get_upcoming_games(year),
        user_info=get_user_information()
    )


@website_blueprint.route("/privacy-policy")
def privacy_policy():
    return render_template("website/privacy-policy.html")


@website_blueprint.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("website/terms_and_conditions.html")


@website_blueprint.route("/.well-known/microsoft-identity-association.json")
def azure_verify():
    """A route for verifying domain to azure."""
    return send_from_directory(
        app.static_folder,
        "microsoft-identity-association.json"
    )


@website_blueprint.route("/robots.txt")
def robot():
    """A route for the google web crawler."""
    return send_from_directory(app.static_folder, "robots.txt")


@website_blueprint.route("/website/leagueNotFound/<int:year>")
def league_not_found(year):
    return render_template(
        "website/leagueNotFound.html",
        base=base_data(year),
        title="League not found",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/rulesAndFields/<int:year>")
def rules_fields(year):
    return render_template(
        "website/fields-and-rules.html",
        base=base_data(year),
        title="Fields & Rules",
        year=year,
        user_info=get_user_information()
    )


for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
