'''
@author: Dallas Fraser
@author: 2015-11-21
@organization: MLSB API
@summary: Holds the error handlers for the database
'''

from api import app
from api.errors import InvalidField, NonUniqueEmail, TeamDoesNotExist,\
                        PlayerDoesNotExist, GameDoesNotExist,\
                        LeagueDoesNotExist, SponsorDoesNotExist
from flask import Response
from json import dumps

@app.errorhandler(InvalidField)
def handle_invalid_field(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(NonUniqueEmail)
def handle_duplicate_email(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(TeamDoesNotExist)
def handle_team_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(PlayerDoesNotExist)
def handle_player_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(GameDoesNotExist)
def handle_game_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(LeagueDoesNotExist)
def handle_league_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

@app.errorhandler(SponsorDoesNotExist)
def handle_sponsor_does_not_exist(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return  response

