# -*- coding: utf-8 -*-
""" Holds views related to captain activities. """
from flask import render_template, Response, request
from flask_login import current_user
from api.variables import UNASSIGNED
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
from api.authentication import \
    get_user_information, require_captain, api_require_captain, \
    require_to_be_a_captain
from api.bot.submit_scores import submit_bats, submit_score
from api.model import Bat, Team, Player, Game
from api.errors import NotTeamCaptain
from api.website import website_blueprint
from datetime import datetime
import json


@website_blueprint.route("/captain/game_summary/<int:team_id>")
@require_captain
def captain_score_games(team_id: int):
    """Navigate to the captain score app"""
    year = datetime.now().year
    return render_template("website/captain_score_app.html",
                           route=Routes,
                           base=base_data(year),
                           title="Captain Submit Score",
                           year=year,
                           team_id=team_id,
                           user_info=get_user_information())


@website_blueprint.route("/captain/batting_app/<int:team_id>")
@require_captain
def captain_batting_app(team_id: int):
    """Navigate to the captain batting app"""
    year = datetime.now().year
    return render_template("website/captain_batting_app.html",
                           route=Routes,
                           base=base_data(year),
                           title="Captain In-Game Batting App",
                           year=year,
                           team_id=team_id,
                           user_info=get_user_information())


@website_blueprint.route("/captain/games/<int:year>")
@require_to_be_a_captain
def captain_games(year: int):
    """Route for captain submitting games for the given year"""
    teams = Player.get_teams_captained(current_user.id)
    print(teams)
    open_games = [
        game.json() for game in Game.games_needing_scores(teams, year=year)
    ]
    submitted_games = [
        game.json() for game in Game.games_with_scores(teams, year=year)
    ]
    return render_template(
        "website/captain_games.html",
        routes=Routes,
        base=base_data(year),
        title="Captain - Submit Scores",
        year=year,
        user_info=get_user_information(),
        open_games=open_games,
        submitted_games=submitted_games
    )


@website_blueprint.route("/captain/api/games/<int:team_id>")
@api_require_captain
def get_captain_info(team_id: int):
    """Get captain information for submitting games"""
    team = Team.query.get(team_id)
    if team is None:
        msg = f"Player is not a captain of any team {current_user.id}"
        raise NotTeamCaptain(msg)
    games = Game.games_needing_scores([team], year=team.year)
    return Response(json.dumps({
        "games": [game.json() for game in games],
        "players": sorted(
            [player.json() for player in team.players],
            key=lambda x: x['player_id']),
        "team_id": team_id,
        "captain_id": team.player_id
    }), status=200, mimetype="application/json")


@website_blueprint.route(
    "/captain/api/submit_score/<int:team_id>", methods=["POST"]
)
@api_require_captain
def captain_submit_score(team_id: int):
    """Submit a score for some game"""
    sheet = request.get_json(silent=True)
    submit_score(
        sheet.get('game_id', UNASSIGNED),
        current_user.id,
        int(sheet.get('score', 0)),
        sheet.get('hr', []),
        sheet.get('ss', []))
    return Response(json.dumps(True), status=200, mimetype="application/json")


@website_blueprint.route("/captain/api/submit_batting/<int:team_id>", methods=["POST"])
@api_require_captain
def captain_submit_full_game(team_id: int):
    """Submit a complete game batting information for some game"""
    bats = request.get_json(silent=True)
    result = submit_bats([Bat(
        bat.get('player_id', UNASSIGNED),
        bat.get('team_id'),
        bat.get('game_id'),
        bat.get('classification'),
        inning=bat.get('inning'),
        rbi=bat.get('rbi')
    ) for bat in bats])
    return Response(json.dumps(result), status=200, mimetype="application/json")
