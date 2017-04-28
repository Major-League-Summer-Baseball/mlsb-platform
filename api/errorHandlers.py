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
                        PlayerNotOnTeam,\
                        EspysDoesNotExist, BatDoesNotExist, NotTeamCaptain,\
                        TeamAlreadyHasCaptain, PlayerNotSubscribed,\
                        BadRequestError
from flask import Response
from json import dumps


@app.errorhandler(PlayerNotOnTeam)
def handle_player_not_on_team(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(InvalidField)
def handle_invalid_field(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(NonUniqueEmail)
def handle_duplicate_email(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(TeamDoesNotExist)
def handle_team_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(PlayerDoesNotExist)
def handle_player_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(GameDoesNotExist)
def handle_game_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(LeagueDoesNotExist)
def handle_league_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(SponsorDoesNotExist)
def handle_sponsor_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(EspysDoesNotExist)
def handle_espys_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(BatDoesNotExist)
def handle_bat_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(NotTeamCaptain)
def handle_not_team_captain(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(TeamAlreadyHasCaptain)
def handle_team_already_has_captain(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(PlayerNotSubscribed)
def handle_player_not_subscribed(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response


@app.errorhandler(BadRequestError)
def handle_bad_request_error(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response
