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
    BadRequestError, TeamNotPartOfLeague
from flask import Response
from json import dumps


@app.errorhandler(BatDoesNotExist)
@app.errorhandler(NotTeamCaptain)
@app.errorhandler(TeamAlreadyHasCaptain)
@app.errorhandler(PlayerNotSubscribed)
@app.errorhandler(BadRequestError)
@app.errorhandler(EspysDoesNotExist)
@app.errorhandler(SponsorDoesNotExist)
@app.errorhandler(LeagueDoesNotExist)
@app.errorhandler(GameDoesNotExist)
@app.errorhandler(PlayerDoesNotExist)
@app.errorhandler(TeamDoesNotExist)
@app.errorhandler(NonUniqueEmail)
@app.errorhandler(InvalidField)
@app.errorhandler(PlayerNotOnTeam)
@app.errorhandler(FunDoesNotExist)
@app.errorhandler(TeamNotPartOfLeague)
def handle_generic_error(error):
    response = Response(dumps(error.to_dict()), status=error.status_code,
                        mimetype="application/json")
    return response
