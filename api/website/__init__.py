# -*- coding: utf-8 -*-
"""
    The main entry into the website.

    Contains the index page and other things for crawlers/facebook
"""
__all__ = []
from flask import \
    redirect, render_template, send_from_directory, url_for, Blueprint, request
from datetime import date

from sqlalchemy import desc
from api import app
from api.cached_items import get_upcoming_games, get_leagues
from api.authentication import get_user_information
import pkgutil
import importlib
import inspect

from api.models.blog_post import BlogPost

website_blueprint = Blueprint("website", __name__, url_prefix="/")


@website_blueprint.app_context_processor
def inject_htmx():
    return dict(snippet=request.headers.get("Hx-Request", False))


@website_blueprint.app_context_processor
def inject_leagues():
    return dict(leagues=get_leagues())


@website_blueprint.app_context_processor
def inject_current_year():
    return dict(current_year=date.today().year)


@website_blueprint.route("/")
@website_blueprint.route("/website")
@website_blueprint.route("/website/")
def reroute():
    year = date.today().year
    return redirect(url_for("website.index", year=year))


@website_blueprint.route("/website/<int:year>")
def index(year):
    posts = BlogPost.query.order_by(desc(BlogPost.date)).limit(6).all()
    return render_template(
        "website/index.html",
        title="Recent news",
        year=year,
        games=get_upcoming_games(year),
        posts=[post.json() for post in posts],
        show_more=True,
        user_info=get_user_information()
    )


@website_blueprint.route("/about")
def general_about():
    year = date.today().year
    return redirect(url_for("website.about", year=year))


@website_blueprint.route("/about/<int:year>")
def about(year):
    return render_template(
        "website/about.html",
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
        title="League not found",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/rulesAndFields/<int:year>")
def rules_fields(year):
    return render_template(
        "website/fields-and-rules.html",
        title="Fields & Rules",
        year=year,
        user_info=get_user_information()
    )


for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    # Import the module dynamically using importlib
    module = importlib.import_module(f"api.website.{name}")

    # Loop over the members of the module and add non-dunder ones to globals()
    for member_name, value in inspect.getmembers(module):
        if member_name.startswith('__'):
            continue

        # Add the value to globals() with the member name
        globals()[member_name] = value

        # Add the member name to __all__
        __all__.append(member_name)
