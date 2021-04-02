'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the error handlers for the database
'''

from api import app
from api.errors import InvalidField, NonUniqueEmail, TeamDoesNotExist,\
    PlayerDoesNotExist, GameDoesNotExist,\
    LeagueDoesNotExist, SponsorDoesNotExist,\
    PlayerNotOnTeam, FunDoesNotExist,\
    EspysDoesNotExist, BatDoesNotExist, NotTeamCaptain,\
    TeamAlreadyHasCaptain, PlayerNotSubscribed,\
    BadRequestError, TeamNotPartOfLeague, DivisionDoesNotExist,\
    OAuthException, HaveLeagueRequestException, NotPartOfLeagueException
from api.model import JoinLeagueRequest, Team
from flask import Response, session, render_template, redirect, url_for
from api.cached_items import get_website_base_data as get_base_data
from json import dumps


@app.route("/existing_league_request")
def handle_existing_league_request():
    is_pending = JoinLeagueRequest.query.filter(
        JoinLeagueRequest.email == session["oauth_email"]).one()
    return render_template("website/pending_league_request.html",
                           base_data=get_base_data(),
                           is_pending=is_pending.pending)


@app.route("/want_to_join")
def handle_not_part_of_league():
    teams = [team.json() for team in Team.query.all()]
    return render_template("website/not_part_of_league.html",
                           base_data=get_base_data(),
                           teams=teams)


@app.errorhandler(BatDoesNotExist)
@app.errorhandler(NotTeamCaptain)
@app.errorhandler(TeamAlreadyHasCaptain)
@app.errorhandler(PlayerNotSubscribed)
@app.errorhandler(BadRequestError)
@app.errorhandler(EspysDoesNotExist)
@app.errorhandler(SponsorDoesNotExist)
@app.errorhandler(DivisionDoesNotExist)
@app.errorhandler(LeagueDoesNotExist)
@app.errorhandler(GameDoesNotExist)
@app.errorhandler(PlayerDoesNotExist)
@app.errorhandler(TeamDoesNotExist)
@app.errorhandler(NonUniqueEmail)
@app.errorhandler(InvalidField)
@app.errorhandler(PlayerNotOnTeam)
@app.errorhandler(FunDoesNotExist)
@app.errorhandler(TeamNotPartOfLeague)
@app.errorhandler(OAuthException)
@app.errorhandler(OAuthException)
@app.errorhandler(Exception)
def handle_generic_error(error):
    if isinstance(error, NotPartOfLeagueException):
        return redirect(url_for("handle_not_part_of_league"))
    elif isinstance(error, HaveLeagueRequestException):
        return redirect(url_for("handle_existing_league_request"))
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response
