'''
@author: Dallas Fraser
@author: 2015-08-27
@organization: MLSB API
@summary: Holds the model for the database
'''
# imports for normal things
from flask import Flask, g, request
from flask_restful import Api
from flask_restful.utils import cors
from flask_sqlalchemy import SQLAlchemy
from api.errors import ERRORS
from flask_caching import Cache
from os import getcwd
from os.path import join
from api.routes import Routes
import uuid
import logging
import sys
import os

SECRET_KEY = os.environ.get('SECRET_KEY', str(uuid.uuid1()))
URL = os.environ.get('DATABASE_URL', "sqlite://")
# Heroku uses postgres but SQL Alchhemy requires full dialect of postgresql
URL = URL.replace("postgres://", "postgresql://") if URL.startswith("postgres://") else URL

if "REDIS_URL" not in os.environ:
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    print("Using a simple cache")
else:
    # on a machine use a real cache
    cache = Cache(config={'CACHE_TYPE': 'redis',
                          'CACHE_REDIS_URL': os.environ['REDIS_URL']})


# create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setup caching
cache.init_app(app)
DB = SQLAlchemy(app)

if 'DATABASE_URL' not in os.environ:
    from initDB import init_database
    init_database(True, True)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
api = Api(app, errors=ERRORS)
api.decorators = [cors.crossdomain(origin='*',
                                   headers=['accept',
                                            'Content-Type'])]
PICTURES = join(getcwd(), "api", "static", "pictures")
CSS_FOLDER = join(getcwd(), "api", "static", "css")
POSTS = join(getcwd(), "api", "templates", "website", "posts")
app.config['UPLOAD_FOLDER'] = "./static"


# these imports cannot be at the top right now

# imports for website, documentation, admin
from api.website import views
from api import admin
from api import documentation
from api import errorHandlers

# imports for basic apis
from api.basic.player import PlayerAPI, PlayerListAPI
from api.basic.sponsor import SponsorAPI, SponsorListAPI
from api.basic.league import LeagueAPI, LeagueListAPI
from api.basic.team import TeamAPI, TeamListAPI
from api.basic.game import GameAPI, GameListAPI
from api.basic.bat import BatAPI, BatListAPI
from api.basic.epsys import EspyAPI, EspyListAPI
from api.basic.fun import FunAPI, FunListAPI
from api.basic.division import DivisionAPI, DivisionListAPI
from api.advanced.team_roster import TeamRosterAPI

# imports for advanced apis
from api.advanced.game_stats import GameStatsAPI
from api.advanced.players_stats import PlayerStatsAPI
from api.advanced.team_stats import TeamStatsAPI
from api.advanced.player_lookup import PlayerLookupAPI
from api.advanced.fun import AdvancedFunAPI
from api.advanced.player_teams import PlayerTeamLookupAPI
from api.advanced.league_leaders import LeagueLeadersAPI
from api.advanced.schedule import ScheduleAPI
from api.advanced.divisions_in_league import DivisionsLeagueAPI

# imports for bot apis
from api.bot.submit_scores import SubmitScoresAPI as BotSubmitScoresAPI
from api.bot.authenticate_captain import \
    AuthenticateCaptainAPI as BotAuthenticateCaptainAPI
from api.bot.get_captain_games import CaptainGamesAPI as BotCaptainGamesAPI
from api.bot.get_upcoming_games import UpcomingGamesAPI as BotUpcomingGamesAPI
from api.bot.submit_transaction import SubmitTransactionAPI as BotSubmitTransactionAPI


@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers.
        This ensures any failures are also accessible
        by the client.
    """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin',
                                                                      '*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    t = 'Access-Control-Allow-Headers'
    resp.headers[t] = request.headers.get('Access-Control-Request-Headers',
                                          'Authorization')
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp


# basic routes
api.add_resource(FunListAPI,
                 Routes['fun'],
                 endpoint="funs")
api.add_resource(FunAPI,
                 Routes['fun'] + "/<int:year>",
                 endpoint="fun")
api.add_resource(PlayerListAPI,
                 Routes['player'],
                 endpoint="players")
api.add_resource(PlayerAPI,
                 Routes['player'] + "/<int:player_id>",
                 endpoint="player")
api.add_resource(SponsorListAPI,
                 Routes['sponsor'],
                 endpoint="sponsors")
api.add_resource(SponsorAPI,
                 Routes['sponsor'] + "/<int:sponsor_id>",
                 endpoint="sponsor")
api.add_resource(DivisionListAPI,
                 Routes['division'],
                 endpoint="divisions")
api.add_resource(DivisionAPI,
                 Routes['division'] + "/<int:division_id>",
                 endpoint="division")
api.add_resource(LeagueListAPI,
                 Routes['league'],
                 endpoint="leagues")
api.add_resource(LeagueAPI,
                 Routes['league'] + "/<int:league_id>",
                 endpoint="league")
api.add_resource(TeamListAPI,
                 Routes['team'],
                 endpoint="teams")
api.add_resource(TeamAPI,
                 Routes['team'] + "/<int:team_id>",
                 endpoint="team")
api.add_resource(GameListAPI,
                 Routes['game'],
                 endpoint="games")
api.add_resource(GameAPI,
                 Routes['game'] + "/<int:game_id>",
                 endpoint="game")
api.add_resource(BatListAPI,
                 Routes['bat'],
                 endpoint="bats")
api.add_resource(BatAPI,
                 Routes['bat'] + "/<int:bat_id>",
                 endpoint="bat")
api.add_resource(EspyListAPI,
                 Routes['espy'],
                 endpoint="Espys")
api.add_resource(EspyAPI,
                 Routes['espy'] + "/<int:espy_id>",
                 endpoint="basic-espy")
api.add_resource(TeamRosterAPI,
                 Routes['team_roster'] + "/<int:team_id>",
                 endpoint="teamrosters")

# add advanced routes
api.add_resource(GameStatsAPI, Routes['vgame'], endpoint="vgame")
api.add_resource(PlayerStatsAPI, Routes['vplayer'], endpoint="vplayer")
api.add_resource(TeamStatsAPI, Routes['vteam'], endpoint="vteam")
api.add_resource(PlayerLookupAPI, Routes['vplayerLookup'],
                 endpoint="vplayerlookup")
api.add_resource(AdvancedFunAPI, Routes['vfun'], endpoint="vfun")
api.add_resource(PlayerTeamLookupAPI, Routes['vplayerteamLookup'],
                 endpoint='vplayerteamLookup')
api.add_resource(LeagueLeadersAPI, Routes['vleagueleaders'],
                 endpoint='vleagueleaders')
api.add_resource(ScheduleAPI,
                 Routes['vschedule'] + "/<int:year>" + "/<int:league_id>",
                 endpoint='vSchedule')
api.add_resource(DivisionsLeagueAPI,
		 Routes['vdivisions'] + "/<int:year>/<int:league_id>",
		 endpoint='vDivisions')


# add bot routes
api.add_resource(BotAuthenticateCaptainAPI,
                 Routes['botcaptain'],
                 endpoint="botcaptain")
api.add_resource(BotSubmitScoresAPI,
                 Routes['botsubmitscore'],
                 endpoint="botsubmitscore")
api.add_resource(BotCaptainGamesAPI,
                 Routes['botcaptaingames'],
                 endpoint="botcaptaingames")
api.add_resource(BotUpcomingGamesAPI,
                 Routes['botupcominggames'],
                 endpoint="botupcominggames")
api.add_resource(BotSubmitTransactionAPI,
                 Routes['bottransaction'],
                 endpoint="bottransaction")

