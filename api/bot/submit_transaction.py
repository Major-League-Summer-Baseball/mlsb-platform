from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.extensions import DB
from api.model import Player, Espys, Sponsor, Team
from api.authentication import requires_admin
from api.errors import PlayerNotOnTeam, SponsorDoesNotExist, \
    PlayerDoesNotExist, TeamDoesNotExist
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int, required=True)
parser.add_argument('amount', type=int, required=True)
parser.add_argument('sponsor', type=str, required=True)
parser.add_argument('team_id', type=int, required=True)


class SubmitTransactionAPI(Resource):

    @requires_admin
    def post(self):
        """
            POST request for submitting a transaction
            Route: Route['bottransaction']
            Parameters:
                player_id: the id of the player submitting the receipt (int)
                amount: the amount spent (int)
                sponsor: the name of the sponsor (str)
                team_id: the id of the team (int)
            Returns:
                status: 200
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        player_id = args['player_id']
        team_id = args['team_id']
        amount = args['amount']
        sponsor_name = args['sponsor']

        # ensure the player exists
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        # ensure the team exist
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})

        # ensure the sponsor exists
        sponsor = Sponsor.query.filter_by(name=sponsor_name).first()
        if sponsor is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_name})

        # player can only submit receipts to their own team
        if not team.is_player_on_team(player):
            raise PlayerNotOnTeam(payload={'details': player_id})

        # should be good to add the espy now
        espy = Espys(team_id=team.id,
                     sponsor_id=sponsor.id,
                     points=amount,
                     description="Bot transaction")
        DB.session.add(espy)
        DB.session.commit()
        handle_table_change(Tables.ESPYS)
        return Response(dumps(espy.id),
                        status=200,
                        mimetype="application/json")
