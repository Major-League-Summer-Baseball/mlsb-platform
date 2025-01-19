from datetime import date
from flask import Response, session, render_template, redirect, url_for, \
    current_app
from api.errors import ImageDoesNotExist, InvalidField, NonUniqueEmail, TeamDoesNotExist, \
    PlayerDoesNotExist, GameDoesNotExist, \
    LeagueDoesNotExist, SponsorDoesNotExist, \
    PlayerNotOnTeam, FunDoesNotExist, \
    EspysDoesNotExist, BatDoesNotExist, NotTeamCaptain, \
    TeamAlreadyHasCaptain, PlayerNotSubscribed, NotLeagueConvenor, \
    BadRequestError, TeamNotPartOfLeague, DivisionDoesNotExist, \
    OAuthException, HaveLeagueRequestException, NotPartOfLeagueException, \
    LeagueEventDateDoesNotExist, LeagueEventDoesNotExist, \
    RequestDoesNotExist
from api.model import JoinLeagueRequest, Team
from api.logging import LOGGER
from api.cached_items import get_website_base_data as get_base_data
from api.authentication import get_user_information
from json import dumps
from traceback import print_exc


@current_app.route("/existing_league_request")
def handle_existing_league_request():
    is_pending = JoinLeagueRequest.query.filter(
        JoinLeagueRequest.email == session["oauth_email"]).one()
    year = date.today().year
    return render_template("website/pending_league_request.html",
                           base=get_base_data(year),
                           year=year,
                           is_pending=is_pending.pending,
                           user_info=get_user_information())


@current_app.route("/want_to_join")
def handle_not_part_of_league():
    year = date.today().year
    teams = [team.json()
             for team in Team.query.all()
             if team.year == year]
    return render_template("website/not_part_of_league.html",
                           base=get_base_data(year),
                           year=year,
                           teams=teams,
                           user_info=get_user_information())


@current_app.errorhandler(BatDoesNotExist)
@current_app.errorhandler(NotTeamCaptain)
@current_app.errorhandler(NotLeagueConvenor)
@current_app.errorhandler(TeamAlreadyHasCaptain)
@current_app.errorhandler(PlayerNotSubscribed)
@current_app.errorhandler(BadRequestError)
@current_app.errorhandler(EspysDoesNotExist)
@current_app.errorhandler(ImageDoesNotExist)
@current_app.errorhandler(SponsorDoesNotExist)
@current_app.errorhandler(DivisionDoesNotExist)
@current_app.errorhandler(LeagueDoesNotExist)
@current_app.errorhandler(LeagueEventDoesNotExist)
@current_app.errorhandler(LeagueEventDateDoesNotExist)
@current_app.errorhandler(GameDoesNotExist)
@current_app.errorhandler(PlayerDoesNotExist)
@current_app.errorhandler(TeamDoesNotExist)
@current_app.errorhandler(RequestDoesNotExist)
@current_app.errorhandler(NonUniqueEmail)
@current_app.errorhandler(InvalidField)
@current_app.errorhandler(PlayerNotOnTeam)
@current_app.errorhandler(FunDoesNotExist)
@current_app.errorhandler(TeamNotPartOfLeague)
@current_app.errorhandler(OAuthException)
@current_app.errorhandler(HaveLeagueRequestException)
@current_app.errorhandler(NotPartOfLeagueException)
def handle_generic_error(error):
    if isinstance(error, NotPartOfLeagueException):
        return redirect(url_for("handle_not_part_of_league"))
    elif isinstance(error, HaveLeagueRequestException):
        return redirect(url_for("handle_existing_league_request"))
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@current_app.errorhandler(Exception)
def unhandled_generic_error(error):
    LOGGER.error(error)
    print_exc()
    response = Response(dumps(str(error)), status=400,
                        mimetype="application/json")
    return response
