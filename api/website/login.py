# -*- coding: utf-8 -*-
"""Holds views related to login, authentication and join leagues"""
from flask import render_template, session, request, url_for, redirect
from flask_login import \
    current_user, logout_user, login_required, login_user
from datetime import date
from api.extensions import DB
from api.errors import OAuthException
from api.authentication import \
    is_facebook_supported, is_github_supported, is_gmail_supported, \
    is_azure_supported
from api.model import JoinLeagueRequest, Player
from api.logging import LOGGER
from api.cached_items import get_website_base_data as get_base_data
from api.authentication import get_user_information
from api.website import website_blueprint


@website_blueprint.route("/authenticate")
def need_to_login():
    """A route used to indicate the user needs to authenicate for some page."""
    year = date.today().year
    return render_template(
        "website/login.html",
        message="Need to login to proceed further.",
        year=year,
        base=get_base_data(year),
        github_enabled=is_github_supported(),
        azure_enabled=is_azure_supported(),
        facebook_enabled=is_facebook_supported(),
        gmail_enabled=is_gmail_supported(),
        user_info=get_user_information()
    )


@website_blueprint.route("/login")
def loginpage():
    """A route to login the user."""
    year = date.today().year
    return render_template(
        "website/login.html",
        base=get_base_data(year),
        year=year,
        github_enabled=is_github_supported(),
        azure_enabled=is_azure_supported(),
        facebook_enabled=is_facebook_supported(),
        gmail_enabled=is_gmail_supported(),
        user_info=get_user_information()
    )


@website_blueprint.route("/logout")
@login_required
def logout():
    """A route to log out the user."""
    LOGGER.info(f"{current_user} has logged out")
    logout_user()
    return redirect(url_for("website.index", year=date.today().year))


@website_blueprint.route("/join_league", methods=["POST"])
def join_league():
    """A form submission to ask to join the league."""
    # ensure given an email
    email = session.get("oauth_email", None)
    if email is None:
        # it should have been stored after authenicating
        message = "Sorry, the authentication provider did not give an email"
        raise OAuthException(message)
    # double check the player email has not be taken
    player = Player.query.filter(Player.email == email).first()
    if player is not None:
        login_user(player)
        return redirect(url_for("homepage"))
    gender = "F" if request.form.get("is_female", False) else "M"
    player_name = request.form.get("name", None)
    team_id = request.form.get("team", None)

    # create a request
    DB.session.add(
        JoinLeagueRequest.create_request(player_name, email, gender, team_id)
    )
    DB.session.commit()
    return redirect(url_for("website.league_request_sent"))


@website_blueprint.route("/request_sent", methods=["GET"])
def league_request_sent():
    message = ("Submitted request to join."
               " Please wait until a convenor/captain responds")
    year = date.today().year
    return render_template(
        "website/error.html",
        year=year,
        base=get_base_data(year),
        message=message,
        user_info=get_user_information()
    )
