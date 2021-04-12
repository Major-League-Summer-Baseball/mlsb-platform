# -*- coding: utf-8 -*-
"""Holds views related to login, authentication and join leagues"""
from flask import render_template, session, request, url_for, redirect
from flask_login import current_user, logout_user, login_required,\
    login_user
from sqlalchemy import func
from datetime import date
from api import app, DB
from api.errors import HaveLeagueRequestException, TeamDoesNotExist,\
    OAuthException
from api.authentication import is_facebook_supported, is_github_supported,\
    is_gmail_supported
from api.model import JoinLeagueRequest, Player, Team
from api.routes import Routes
from api.logging import LOGGER
from api.cached_items import get_website_base_data as get_base_data
from api.authentication import get_user_information


@app.route("/authenticate")
def need_to_login():
    """A route used to indicate the user needs to authenicate for some page."""
    year = date.today().year
    return render_template("website/login.html",
                           message="Need to login to proceed further.",
                           route=Routes,
                           year=year,
                           base=get_base_data(year),
                           github_enabled=is_github_supported(),
                           facebook_enabled=is_facebook_supported(),
                           gmail_enabled=is_gmail_supported(),
                           user_info=get_user_information())


@app.route("/login")
def loginpage():
    """A route to login the user."""
    year = date.today().year
    return render_template("website/login.html",
                           base=get_base_data(year),
                           route=Routes,
                           year=year,
                           github_enabled=is_github_supported(),
                           facebook_enabled=is_facebook_supported(),
                           gmail_enabled=is_gmail_supported(),
                           user_info=get_user_information())


@app.route("/logout")
@login_required
def logout():
    """A route to log out the user."""
    LOGGER.info(f"{current_user} has logged out")
    logout_user()
    return redirect(url_for("index", year=date.today().year))


@app.route("/join_league", methods=["POST"])
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
    # double check this is not refresh page issue
    pending_request = JoinLeagueRequest.query.filter(
        func.lower(JoinLeagueRequest.email) == email.lower()).first()
    if pending_request is not None:
        raise HaveLeagueRequestException("Double submit on form")
    # ensure the selected team exists
    team_id = request.form.get("team", None)
    if team_id is None:
        raise TeamDoesNotExist(f"Team does not exist - {team_id}")
    team = Team.query.get(team_id)
    if team is None:
        raise TeamDoesNotExist(f"Team does not exist - {team_id}")

    # save the request
    player_name = request.form.get("name", None)
    gender = "F" if request.form.get("is_female", False) else "M"
    league_request = JoinLeagueRequest(email, player_name, team, gender)
    DB.session.add(league_request)
    DB.session.commit()
    return redirect(url_for("league_request_sent"))


@app.route("/request_sent", methods=["GET"])
def league_request_sent():
    message = ("Submitted request to join."
               " Please wait until a convenor responds")
    year = date.today().year
    return render_template("website/error.html",
                           route=Routes,
                           year=year,
                           base=get_base_data(year),
                           message=message,
                           user_info=get_user_information())
