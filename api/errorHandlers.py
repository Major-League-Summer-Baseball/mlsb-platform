'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the error handlers for the database
'''
from datetime import date
from api import app
from api.errors import InvalidField, NonUniqueEmail, TeamDoesNotExist,\
    PlayerDoesNotExist, GameDoesNotExist,\
    LeagueDoesNotExist, SponsorDoesNotExist,\
    PlayerNotOnTeam, FunDoesNotExist,\
    EspysDoesNotExist, BatDoesNotExist, NotTeamCaptain,\
    TeamAlreadyHasCaptain, PlayerNotSubscribed,\
    BadRequestError, TeamNotPartOfLeague, DivisionDoesNotExist,\
    OAuthException, HaveLeagueRequestException, NotPartOfLeagueException,\
    LeagueEventDateDoesNotExist, LeagueEventDoesNotExist
from api.model import JoinLeagueRequest, Team
from api.logging import LOGGER
from api.routes import Routes
from flask import Response, session, render_template, redirect, url_for
from api.cached_items import get_website_base_data as get_base_data
from api.authentication import get_user_information
from json import dumps
import traceback


@app.route("/existing_league_request")
def handle_existing_league_request():
    is_pending = JoinLeagueRequest.query.filter(
        JoinLeagueRequest.email == session["oauth_email"]).one()
    year = date.today().year
    return render_template("website/pending_league_request.html",
                           base=get_base_data(year),
                           route=Routes,
                           year=year,
                           is_pending=is_pending.pending,
                           user_info=get_user_information())


@app.route("/want_to_join")
def handle_not_part_of_league():
    year = date.today().year
    teams = [team.json()
             for team in Team.query.all()
             if team.year == year]
    return render_template("website/not_part_of_league.html",
                           base=get_base_data(year),
                           route=Routes,
                           year=year,
                           teams=teams,
                           user_info=get_user_information())


@app.errorhandler(BatDoesNotExist)
@app.errorhandler(NotTeamCaptain)
@app.errorhandler(TeamAlreadyHasCaptain)
@app.errorhandler(PlayerNotSubscribed)
@app.errorhandler(BadRequestError)
@app.errorhandler(EspysDoesNotExist)
@app.errorhandler(SponsorDoesNotExist)
@app.errorhandler(DivisionDoesNotExist)
@app.errorhandler(LeagueDoesNotExist)
@app.errorhandler(LeagueEventDoesNotExist)
@app.errorhandler(LeagueEventDateDoesNotExist)
@app.errorhandler(GameDoesNotExist)
@app.errorhandler(PlayerDoesNotExist)
@app.errorhandler(TeamDoesNotExist)
@app.errorhandler(NonUniqueEmail)
@app.errorhandler(InvalidField)
@app.errorhandler(PlayerNotOnTeam)
@app.errorhandler(FunDoesNotExist)
@app.errorhandler(TeamNotPartOfLeague)
@app.errorhandler(OAuthException)
@app.errorhandler(HaveLeagueRequestException)
@app.errorhandler(NotPartOfLeagueException)
def handle_generic_error(error):
    if isinstance(error, NotPartOfLeagueException):
        return redirect(url_for("handle_not_part_of_league"))
    elif isinstance(error, HaveLeagueRequestException):
        return redirect(url_for("handle_existing_league_request"))
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(Exception)
def unhandled_generic_error(error):
    LOGGER.error(error)
    traceback.print_exc()
    response = Response(dumps(str(error)), status=400,
                        mimetype="application/json")
    return response
