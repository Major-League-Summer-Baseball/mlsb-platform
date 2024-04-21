# -*- coding: utf-8 -*-
"""Holds views that are only used for cypress testing."""
from flask import Response, request, Blueprint
from flask_login import login_user, logout_user
from sqlalchemy import and_
from api.extensions import DB
from api.model import Player, JoinLeagueRequest, Team, Game, Division
from api.logging import LOGGER
from api.errors import TeamDoesNotExist
from datetime import datetime
import json
import uuid

testing_blueprint = Blueprint("testing", __name__, url_prefix='/testing')


@testing_blueprint.post("/api/create_and_login")
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


@testing_blueprint.post("/api/convenor/login")
def login_convenor():
    """Login as convenor - create one if doesn't exist."""
    convenor = Player.query.filter(Player.is_convenor == True).first()
    print(convenor)
    if convenor is None:
        LOGGER.info(f"Adding convenor for testing")
        convenor = Player(
            str(uuid.uuid1()),
            str(uuid.uuid1()) + "convenor-testing@mlsb.ca",
            gender="m"
        )
        convenor.make_convenor()
        DB.session.add(convenor)
        DB.session.commit()
    login_user(convenor)
    return Response(
        json.dumps(convenor.admin_json()), 200, mimetype='application/json'
    )


@testing_blueprint.post("/api/logout")
def logout():
    """Logout a test user."""
    result = logout_user()
    return Response(json.dumps(result), 200, mimetype='application/json')


@testing_blueprint.post(
    "/api/<int:team_id>/add_player/<int:player_id>"
)
def add_player_to_team(team_id: int, player_id: int):
    """Add a player to the given team."""
    player = Player.query.get(player_id)
    team = Team.query.get(team_id)
    if player is None or team is None:
        return Response(json.dumps(None), 404)
    team.insert_player(player.id, captain=False)
    DB.session.commit()
    return Response(json.dumps(True), 200, mimetype='application/json')


@testing_blueprint.post("/api/make_captain")
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


@testing_blueprint.post("/api/create_league_request")
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


@testing_blueprint.route("/api/get_current_team", methods=["GET"])
def get_active_team():
    """Get some active team."""
    year = datetime.now().year
    team = Team.query.filter(
        and_(Team.year == year, Team.player_id is not None)
    ).first()
    if team is None:
        raise TeamDoesNotExist("No team for current year")
    return Response(
        json.dumps(team.json(admin=True)),
        200, mimetype='application/json')


@testing_blueprint.post("/api/team/<int:team_id>/game_without_score")
def game_without_score(team_id: int):
    """Ensure the given team has a game today"""
    team = Team.query.get(team_id)
    if team is None:
        return Response(json.dumps(False), 404, mimetype='application/json')
    games = Game.games_needing_scores([team], year=team.year)
    if len(games) == 0:
        today = datetime.now()
        other_team = Team.query.filter(and_(Team.year == today.year,
                                            Team.id != team_id)).first()
        division = Division.query.first()
        game = Game(
            today.strftime("%Y-%m-%d"),
            "12:00",
            team_id,
            other_team.id,
            other_team.league_id,
            division.id,
            'today game',
            'WP1')
        DB.session.add(game)
        DB.session.commit()
    else:
        game = games[0]
    return Response(json.dumps(game.json()), 200, mimetype='application/json')
