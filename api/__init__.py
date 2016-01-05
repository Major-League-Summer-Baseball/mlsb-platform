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
from api.errors import ERRORS
local = False
try:
    # running local
    local = True
    from api.credentials import URL, SECRET_KEY
    print("Running Locally")
except:
    URL = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
from os import getcwd
from os.path import join
#create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SECRET_KEY'] = SECRET_KEY
DB = SQLAlchemy(app)
if local:
    DB.create_all()
    print("Created Database")
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
api = Api(app, errors=ERRORS)
api.decorators=[cors.crossdomain(origin='*',headers=['accept', 'Content-Type'])]
PICTURES = join(getcwd(), "api", "static", "pictures")
app.config['UPLOAD_FOLDER'] =  "./static"

from api.website import views
from api import admin
from api import errrorHandlers
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

# basic routes
from api.basic.player import PlayerAPI, PlayerListAPI
from api.basic.sponsor import SponsorAPI, SponsorListAPI
from api.basic.league import LeagueAPI, LeagueListAPI
from api.basic.team import TeamAPI, TeamListAPI
from api.basic.game import GameAPI, GameListAPI
from api.basic.bat import BatAPI, BatListAPI
from api.advanced.team_roster import TeamRosterAPI
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
api.add_resource(GameListAPI, Routes['game'], endpoint="games")
api.add_resource(GameAPI, Routes['game'] + "/<int:game_id>", 
                 endpoint="game")
api.add_resource(BatListAPI, Routes['bat'], endpoint="bats")
api.add_resource(BatAPI, Routes['bat'] + "/<int:bat_id>", 
                 endpoint="bat")
api.add_resource(TeamRosterAPI, Routes['team_roster']+ "/<int:team_id>",
                 endpoint="teamrosters")

# add advanced routes
from api.advanced.game_stats import GameStatsAPI
from api.advanced.players_stats import PlayerStatsAPI
from api.advanced.team_stats import TeamStatsAPI
from api.advanced.player_lookup import PlayerLookupAPI
api.add_resource(GameStatsAPI, Routes['vgame'], endpoint="vgame")
api.add_resource(PlayerStatsAPI, Routes['vplayer'], endpoint="vplayer")
api.add_resource(TeamStatsAPI, Routes['vteam'], endpoint="vteam")
api.add_resource(PlayerLookupAPI, Routes['vplayerLookup'], endpoint="vplayerlookup")

# add documentation
from api.documentation import Document , PlayerObjectDocument,\
                              TeamObjectDocument, BatObjectDocument,\
                              GameObjectDocument, LeagueObjectDocument,\
                              SponsorObjectDocument ,TeamRosterObjectDocument
from api.documentation import PlayerRoute, TeamRoute, BatRoute,\
                              GameRoute, LeagueRoute, SponsorRoute,\
                              TeamRosterRoute, Response
from api.documentation import PlayerView, GameView, TeamView

api.add_resource(Document, Routes["dindex"], endpoint="documentation")
api.add_resource(Response, Routes["dresponse"], endpoint="dresponse")

# player
api.add_resource(PlayerObjectDocument, Routes['doplayer'], endpoint="doplayer")
api.add_resource(PlayerRoute, Routes['dbplayer'], endpoint="dbplayer")

# team
api.add_resource(TeamObjectDocument, Routes['doteam'], endpoint="doteam")
api.add_resource(TeamRoute, Routes['dbteam'], endpoint="dbteam")

# bat
api.add_resource(BatObjectDocument, Routes['dobat'], endpoint="dobat")
api.add_resource(BatRoute, Routes['dbbat'], endpoint="dbbat")

# game
api.add_resource(GameObjectDocument, Routes['dogame'], endpoint="dogame")
api.add_resource(GameRoute, Routes['dbgame'], endpoint="dbgame")

# tournament
api.add_resource(LeagueObjectDocument, Routes['doleague'],
                 endpoint="doleague")
api.add_resource(LeagueRoute, Routes['dbleague'], endpoint="dbleague")

# sponsor
api.add_resource(SponsorObjectDocument, Routes['dosponsor'], 
                 endpoint="dosponsor")
api.add_resource(SponsorRoute, Routes['dbsponsor'], 
                 endpoint="dbsponsor")

# team roster
api.add_resource(TeamRosterObjectDocument, Routes['doteamroster'], 
                 endpoint="doteamroster")

api.add_resource(TeamRosterRoute, Routes['dbteamroster'], 
                 endpoint="dbteamroster")

# view documentation
api.add_resource(TeamView, Routes['dvteam'],
                 endpoint="dvteam")
api.add_resource(GameView, Routes['dvgame'],
                 endpoint="dvgame")
api.add_resource(PlayerView, Routes['dvplayer'],
                 endpoint="dvplayer")
