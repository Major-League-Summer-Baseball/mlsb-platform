# -*- coding: utf-8 -*-
""" Holds views related to captain activities. """
from flask import redirect, render_template, Response, request, url_for
from flask_login import current_user
from api.variables import UNASSIGNED
from api.cached_items import get_website_base_data as base_data
from api.authentication import \
    get_user_information, require_captain, api_require_captain, \
    require_to_be_a_captain
from api.bot.submit_scores import remove_submitted_score, submit_bats, \
    submit_score
from api.model import Bat, Team, Player, Game
from api.errors import GameDoesNotExist, NotTeamCaptain, TeamDoesNotExist
from api.website import website_blueprint
import json


@website_blueprint.route(
    "/captain/game/<int:year>/<int:game_id>/<int:team_id>"
)
@require_captain
def captain_score_app_game(year: int, team_id: int, game_id: int):
    """Route for handling Vue score app"""
    team = Team.query.get(team_id)
    game = Game.query.get(game_id)
    if game is None:
        raise GameDoesNotExist(payload={
            'details': game_id
        })
    if team is None:
        raise TeamDoesNotExist(payload={
            'details': team_id
        })

    captain_info = {
        "players": sorted(
            [player.json() for player in team.players],
            key=lambda x: x['player_id']),
        "team_id": team_id,
        "captain_id": team.player_id
    }

    return render_template(
        "website/vue/scores.html",
        captain_info=captain_info,
        team_id=team_id,
        game=game.json(),
        base=base_data(year),
        title="Captain Submit Score",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route(
    "/captain/batting_app/<int:year>/<int:game_id>/<int:team_id>"
)
@require_captain
def captain_batting_app_game(year: int, team_id: int, game_id: int):
    """Route for handling Vue batting app"""
    team = Team.query.get(team_id)
    game = Game.query.get(game_id)
    if team is None:
        raise NotTeamCaptain(payload={'details': team_id})
    if game is None:
        raise GameDoesNotExist(payload={'details': game_id})

    captain_info = {
        "players": sorted(
            [player.json() for player in team.players],
            key=lambda x: x['player_id']),
        "team_id": team_id,
        "captain_id": team.player_id
    }

    return render_template(
        "website/vue/batting.html",
        captain_info=captain_info,
        game=game.json(),
        team_id=team_id,
        base=base_data(year),
        title="Captain In-Game Batting App",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route(
    "/captain/games/resubmit/<int:year>/<int:game_id>/<int:team_id>",
    methods=["GET", "POST", "DELETE"]
)
@require_to_be_a_captain
def captain_remove_submitted_score(year: int, game_id: int, team_id: int):
    """API for handling when a captain wants to resubmit a game score"""
    remove_submitted_score(game_id, team_id)
    return redirect(url_for('website.captain_games', year=year), code=307)


@website_blueprint.route(
    "/captain/games/<int:year>",
    methods=["GET", "POST", "DELETE"]
)
@require_to_be_a_captain
def captain_games(year: int):
    """Route for captain submitting games for the given year"""
    teams = Player.get_teams_captained(current_user.id)
    team_ids = [team.id for team in teams]
    open_games = [
        (
            game.json(),
            game.home_team_id
            if game.home_team_id in team_ids
            else game.away_team_id
        )
        for game in Game.games_needing_scores(teams, year=year)
    ]
    submitted_games = [
        (
            game.json(),
            game.home_team_id
            if game.home_team_id in team_ids
            else game.away_team_id
        )
        for game in Game.games_with_scores(teams, year=year)
    ]
    return render_template(
        "website/captain_games.html",
        base=base_data(year),
        title="Captain - Submit Scores",
        year=year,
        user_info=get_user_information(),
        open_games=open_games,
        submitted_games=submitted_games
    )


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


@website_blueprint.route(
    "/captain/api/submit_batting/<int:team_id>",
    methods=["POST"]
)
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
