'''
@author: Dallas Fraser
@author: 2015-08-27
@organization: MLSB API
@summary: Holds the model for the database
'''
import os
from flask import Flask, g, request
from flask.ext.restful import Api
from flask.ext.restful.utils import cors
from flask.ext.sqlalchemy import SQLAlchemy
from api.credentials import PWD, URL

#create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL
DB = SQLAlchemy(app)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

api = Api(app)
api.decorators=[cors.crossdomain(origin='*',headers=['accept', 'Content-Type'])]

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. 
        This ensures any failures are also accessible
        by the client. 
    """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

from api.basic.player import PlayerAPI, PlayerListAPI
from api.basic.sponsor import SponsorAPI, SponsorListAPI
from api.basic.league import LeagueAPI, LeagueListAPI
from api.basic.team import TeamAPI, TeamListAPI
from api.routes import Routes

api.add_resource(PlayerListAPI, Routes['player'], endpoint="players")
api.add_resource(PlayerAPI, Routes['player'] + "/<int:player_id>", 
                 endpoint="player")
api.add_resource(SponsorListAPI, Routes['sponsor'], endpoint="sponsors")
api.add_resource(SponsorAPI, Routes['sponsor'] + "/<int:sponsor_id>", 
                 endpoint="sponsor")
api.add_resource(LeagueListAPI, Routes['league'], endpoint="leagues")
api.add_resource(LeagueAPI, Routes['league'] + "/<int:league_id>", 
                 endpoint="league")
api.add_resource(TeamListAPI, Routes['team'], endpoint="teams")
api.add_resource(TeamAPI, Routes['team'] + "/<int:team_id>", 
                 endpoint="team")

