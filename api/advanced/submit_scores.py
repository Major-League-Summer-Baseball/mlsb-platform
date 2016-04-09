'''
@author: Dallas Fraser
@author: 2015-09-29
@organization: MLSB API
@summary: The views for player stats
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Bat, Game, Team
from api.authentication import requires_kik
from flask import session
from api.errors import InvalidField , GDNESC
from api.variables import UNASSIGNED
parser = reqparse.RequestParser()

parser.add_argument('game_id', type=int, required=True)
parser.add_argument('kik', type=str, required=True)
parser.add_argument('score', type=int, required=True)
parser.add_argument('hr', type=int, action="append")
parser.add_argument('ss', type=int, action="append")

def find_player(team_id, player_name):
    team = Team.query.get(team_id)
    player = None
    for p in team.players:
        if player_name == p.name:
            player = p.id
    return player

class SubmitScoresAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for submitting Score Summaries
            Route: Route['submit_scores']
            Parameters:
                game_id: the game_id (int)
                kik: the kik user name of the captain (str)
                score: the score of the captains team (int)
                hr: a list of player's name who hit homeruns(List of str)
                ss: a list of player's name who hit sentry singles (List of str)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Players
        """
        args = parser.parse_args()
        game_id = args['game_id']
        game = Game.query.get(game_id)
        kik = args['kik']
        captain = Player.query.filter_by(kik=kik).first()
        if captain is None:
            return Response(dumps("Kik name does not match"), status=404, mimetype="application/json")
        if game is None:
            return Response(dumps("Game not found"), status=GDNESC, mimetype="application/json")
        # find the team
        away_team = Team.query.get(game.away_team_id)
        home_team = Team.query.get(game.home_team_id)
        team = None
        if away_team.player_id == captain.id:
            team = away_team # captain of the squad
        elif home_team.player_id  == captain.id:
            team = home_team # captain of the away squad
        else:
            # not a captain of a team
            return Response(dumps("Not a captain of a team"), status=403, mimetype="application/json")
        homeruns = args['hr']
        ss = args['ss']
        score = args['score']
        if homeruns is not None:
            for player_id in homeruns:
                # add the homeruns
                DB.session.add(Bat(player_id,
                                team.id,
                                game.id,
                                "hr",
                                inning=1,
                                rbi=1)
                            )
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
            return Response(dumps("More hr than runs"), status=400, mimetype="application/json")
        while score > 0:
            bat = Bat(UNASSIGNED,
                      team.id,
                      game.id,
                      "s",
                      inning=1,
                      rbi=1)
            DB.session.add(bat)
            score -= 1
        DB.session.commit() # good to add the submission
        return Response(dumps(True), status=200, mimetype="application/json")

