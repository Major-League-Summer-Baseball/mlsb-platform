# -*- coding: utf-8 -*-
""" Holds views related to captain activities. """
from flask import render_template, Response, request
from flask_login import current_user
from api import app
from api.variables import EVENTS, UNASSIGNED
from api.routes import Routes
from api.bot.get_captain_games import games_without_scores
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information, require_captain,\
    api_require_captain
from api.bot.submit_scores import submit_score
from api.model import Team, Game
from api.errors import NotTeamCaptain, GameDoesNotExist
from datetime import datetime
import json


@app.route("/captain/game_summary/<int:team_id>")
@require_captain
def captain_score_games(team_id: int):
    """Navigate to the captain score app"""
    year = datetime.now().year
    return render_template("website/captain_score_summary.html",
                           route=Routes,
                           base=base_data(year),
                           title="Captain Submit Score",
                           year=year,
                           team_id=team_id,
                           user_info=get_user_information())


@app.route("/captain/api/games/<int:team_id>")
@api_require_captain
def get_captain_info(team_id: int):
    """Get captain information for submitting games"""
    team = Team.query.get(team_id)
    if team is None:
        msg = f"Player is not a captian of any team {current_user.id}"
        raise NotTeamCaptain(msg)
    games = games_without_scores(team.id)
    return Response(json.dumps({
        "games": [game.json() for game in games],
        "players": [player.json() for player in team.players],
        "team_id": team_id,
        "captain_id": team.player_id
    }), status=200, mimetype="application/json")


@app.route("/captain/api/submit_score/<int:team_id>", methods=["POST"])
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
