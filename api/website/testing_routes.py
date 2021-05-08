# -*- coding: utf-8 -*-
"""Holds views that are only used for cypress testing."""
from flask import Response, request
from flask_login import login_user
from functools import wraps
from sqlalchemy import and_, or_
from api import app
from api.model import Player, DB, JoinLeagueRequest, Team, Game, Division
from api.bot.get_captain_games import games_without_scores
from api.logging import LOGGER
from api.errors import TeamDoesNotExist
from datetime import datetime, date
import json
import uuid


def requires_testing(f):
    """A decorator for routes that only available while testing."""
    @wraps(f)
    def decorated(*args, **kwargs):
        development = app.config['ENV'] == "development"
        if not development:
            return Response("Testing feature not on", 400)
        return f(*args, **kwargs)
    return decorated


@app.route("/testing/api/create_and_login", methods=["POST"])
@requires_testing
def create_and_login():
    """Creates a player if they do not exist and login them in."""
    player_info = request.get_json(silent=True)
    player = Player.query.filter(
        Player.email == player_info.get('email')).first()
    if player is None:
        LOGGER.info(f"Adding player to league: {player_info}")
        player = Player(player_info.get("player_name", str(uuid.uuid1())),
                        player_info.get("email"),
                        gender=player_info.get("gender", "m"))
        DB.session.add(player)
        DB.session.commit()
    login_user(player)
    return Response(json.dumps(player.json()), 200, mimetype='application/json')


@app.route("/testing/api/make_captain", methods=["POST"])
@requires_testing
def make_player_captain():
    """Make a given player a captain of some team."""
    data = request.get_json(silent=True)
    player = Player.query.get(data.get('player_id'))
    team = Team.query.get(data.get('team_id'))
    if player is None or team is None:
        return Response(json.dumps(None), 404)
    team.insert_player(data.get('player_id'), captain=True)
    DB.session.commit()
    return Response(json.dumps(True), 200, mimetype='application/json')


@app.route("/testing/api/create_league_request", methods=["POST"])
@requires_testing
def create_league_request():
    """Creates a league request for testing purposes."""
    request_info = request.get_json(silent=True)
    team = Team.query.get(request_info.get("team_id"))
    league_request = JoinLeagueRequest(request_info.get("email"),
                                       request_info.get("player_name"),
                                       team, request_info.get('gender'))
    LOGGER.info(f"Creating join league request: {request_info}")
    DB.session.add(league_request)
    DB.session.commit()
    return Response(
                    json.dumps(league_request.json()),
                    200, mimetype='application/json')


@app.route("/testing/api/get_current_team", methods=["GET"])
@requires_testing
def get_active_team():
    """Get some active team."""
    year = datetime.now().year
    team = Team.query.filter(and_(Team.year == year,
                                  Team.player_id is not None)).first()
    if team is None:
        raise TeamDoesNotExist("No team for current year")
    return Response(
                    json.dumps(team.json(admin=True)),
                    200, mimetype='application/json')


@app.route("/testing/api/team/<int:team_id>/game_without_score", methods=["POST"])
@requires_testing
def game_without_score(team_id: int):
    """Ensure the given team has a game today"""
    today = date.today()
    games = games_without_scores(team_id)
    if len(games) == 0:
        other_team = Team.query.filter(and_(Team.year == year,
                                            Team.id!= team_id)).first()
        division = Division.query.first()
        game = Game(
                    today.strftime("%Y-%m-%d"),
                    "12:00",
                    team_id,
                    other_team.id,
                    other_team.league_id,
                    division.id,
                    'today game',
                    'WP1'
                    )
        DB.session.add(game)
        DB.session.commit()
    else:
        game = games[0]
    return Response(json.dumps(game.json()), 200, mimetype='application/json')