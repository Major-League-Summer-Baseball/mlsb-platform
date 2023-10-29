# -*- coding: utf-8 -*-
"""
    The main entry into the website.

    Contains the index page and other things for crawlers/facebook
"""
__all__ = []
from flask import \
    redirect, render_template, send_from_directory, url_for
from datetime import date
from api import app
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
from api.cached_items import get_upcoming_games
from api.authentication import get_user_information
import pkgutil
import inspect


@app.route("/")
@app.route("/website")
@app.route("/website/")
def reroute():
    year = date.today().year
    return redirect(url_for(
        "index", year=year, user_info=get_user_information()))

@app.route("/about")
def general_about():
    year = date.today().year
    return redirect(url_for(
        "about", year=year, user_info=get_user_information()))


@app.route("/about/<int:year>")
def about(year):
    return render_template("website/about.html",
                           route=Routes,
                           base=base_data(year),
                           title="About",
                           year=year,
                           games=get_upcoming_games(year),
                           user_info=get_user_information())


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("website/privacy-policy.html")


@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("website/terms_and_conditions.html")


@app.route("/.well-known/microsoft-identity-association.json")
def azure_verify():
    """A route for verifying domain to azure."""
    return send_from_directory(
        app.static_folder,
        "microsoft-identity-association.json"
    )


@app.route("/robots.txt")
def robot():
    """A route for the google web crawler."""
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/website/leagueNotFound/<int:year>")
def league_not_found(year):
    return render_template("website/leagueNotFound.html",
                           route=Routes,
                           base=base_data(year),
                           title="League not found",
                           year=year,
                           user_info=get_user_information())


@app.route("/website/rulesAndFields/<int:year>")
def rules_fields(year):
    return render_template("website/fields-and-rules.html",
                           route=Routes,
                           base=base_data(year),
                           title="Fields & Rules",
                           year=year,
                           user_info=get_user_information())


for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
