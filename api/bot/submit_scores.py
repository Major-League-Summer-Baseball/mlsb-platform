from typing import List
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.extensions import DB
from api.model import Player, Bat, Game, Team
from api.authentication import requires_admin
from api.errors import InvalidField, NotTeamCaptain, GameDoesNotExist, \
    PlayerNotSubscribed
from api.variables import UNASSIGNED, UNASSIGNED_EMAIL
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('game_id', type=int, required=True)
parser.add_argument('player_id', type=int, required=True)
parser.add_argument('score', type=int, required=True)
parser.add_argument('hr', type=int, action="append")
parser.add_argument('ss', type=int, action="append")


def submit_bats(bats: List[Bat]) -> bool:
    """Submits a list of bats"""
    for bat in bats:
        DB.session.add(bat)
    DB.session.commit()  # good to add the submission
    handle_table_change(Tables.GAME)
    return True


def submit_score(game_id: int, captain_id: int, score: int,
                 homeruns: List[int], ss: List[int]) -> bool:
    """Captain submit a score"""
    unassigned_player = Player.query.filter_by(
        email=UNASSIGNED_EMAIL).first()
    unassigned_id = UNASSIGNED
    if unassigned_player is not None:
        unassigned_id = unassigned_player.id
    game = Game.query.get(game_id)
    captain = Player.query.get(captain_id)
    if captain is None:
        raise PlayerNotSubscribed(payload={'details': captain_id})
    if game is None:
        raise GameDoesNotExist(payload={'details': game_id})
    # find the team
    away_team = Team.query.get(game.away_team_id)
    home_team = Team.query.get(game.home_team_id)
    team = None
    if away_team.player_id == captain.id:
        team = away_team  # captain of the squad
    elif home_team.player_id == captain.id:
        team = home_team  # captain of the away squad
    else:
        # not a captain of a team
        raise NotTeamCaptain(payload={'details': captain_id})
    if score <= 0:
        # hmm that is so sad
        DB.session.add(Bat(unassigned_id,
                           team.id,
                           game.id,
                           "fo",
                           inning=1,
                           rbi=0))
    if homeruns is not None:
        for player_id in homeruns:
            # add the homeruns
            DB.session.add(Bat(player_id,
                               team.id,
                               game.id,
                               "hr",
                               inning=1,
                               rbi=1))
            score -= 1
    if ss is not None:
        for player_id in ss:
            # add the special singles
            try:
                bat = Bat(player_id,
                          team.id,
                          game.id,
                          "ss",
                          inning=1,
                          rbi=0)
                DB.session.add(bat)
            except InvalidField:
                pass
    if score < 0:
        raise InvalidField(payload={'details': "More hr than score"})
    while score > 0:
        bat = Bat(unassigned_id,
                  team.id,
                  game.id,
                  "s",
                  inning=1,
                  rbi=1)
        DB.session.add(bat)
        score -= 1
    DB.session.commit()  # good to add the submission
    handle_table_change(Tables.GAME)
    return True


class SubmitScoresAPI(Resource):

    @requires_admin
    def post(self):
        """
            POST request for submitting Score Summaries
            Route: Route['botsubmitscore']
            Parameters:
                game_id: the game_id (int)
                player_id: the player_id of the captain (str)
                score: the score of the captains team (int)
                hr: a list of player's name who hit homeruns(List of str)
                ss: a list of player's name who hit sentry singles (List - str)
            Returns:
                status: 200
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        submit_score(
            args.get('game_id', UNASSIGNED),
            args.get('player_id', UNASSIGNED),
            args.get('score', 0),
            args.get('hr', []),
            args.get('ss', []))
        return Response(dumps(True), status=200, mimetype="application/json")
