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
from api import documentation
from api import errorHandlers
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
from api.basic.epsys import EspyAPI, EspyListAPI
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
api.add_resource(EspyListAPI, Routes['espy'], endpoint="Espys")
api.add_resource(EspyAPI, Routes['espy'] + "/<int:espy_id>", 
                 endpoint="basic-espy")
api.add_resource(TeamRosterAPI, Routes['team_roster']+ "/<int:team_id>",
                 endpoint="teamrosters")

# add advanced routes
from api.advanced.game_stats import GameStatsAPI
from api.advanced.players_stats import PlayerStatsAPI
from api.advanced.team_stats import TeamStatsAPI
from api.advanced.player_lookup import PlayerLookupAPI
from api.advanced.fun import AdvancedFunAPI
from api.advanced.player_teams import PlayerTeamLookupAPI
api.add_resource(GameStatsAPI, Routes['vgame'], endpoint="vgame")
api.add_resource(PlayerStatsAPI, Routes['vplayer'], endpoint="vplayer")
api.add_resource(TeamStatsAPI, Routes['vteam'], endpoint="vteam")
api.add_resource(PlayerLookupAPI, Routes['vplayerLookup'],
                 endpoint="vplayerlookup")
api.add_resource(AdvancedFunAPI, Routes['vfun'], endpoint="vfun")
api.add_resource(PlayerTeamLookupAPI, Routes['vplayerteamLookup'],
                 endpoint='vplayerteamLookup')
# add kik routes
from api.kik.submit_scores import SubmitScoresAPI
from api.kik.authenticate_captain import AuthenticateCaptainAPI
from api.kik.subscribe import SubscribeToTeamAPI
from api.kik.submit_transaction import SubmitTransactionAPI
from api.kik.get_captain_games import CaptainGamesAPI
from api.kik.get_upcoming_games import UpcomingGamesAPI
api.add_resource(AuthenticateCaptainAPI, Routes['kikcaptain'], endpoint="kikcaptain")
api.add_resource(SubscribeToTeamAPI, Routes['kiksubscribe'], endpoint="kiksubscribe")
api.add_resource(SubmitScoresAPI, Routes['kiksubmitscore'], endpoint="kiksubmitscore")
api.add_resource(SubmitTransactionAPI, Routes['kiktransaction'], endpoint="kiktransaction")
api.add_resource(CaptainGamesAPI, Routes['kikcaptaingames'], endpoint="kikcaptaingames")
api.add_resource(UpcomingGamesAPI, Routes['kikupcominggames'], endpoint="kikupcominggames")

