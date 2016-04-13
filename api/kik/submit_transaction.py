'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The Kik API for submitting transactions
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Player, Espys,Sponsor, find_team_subscribed
from api.authentication import requires_kik
from api.errors import SDNESC, PNS, PlayerNotSubscribed, SponsorDoesNotExist
parser = reqparse.RequestParser()
parser.add_argument('kik', type=str, required=True)
parser.add_argument('amount', type=int, required=True)
parser.add_argument('sponsor', type=str, required=True)

class SubmitTransactionAPI(Resource):
    @requires_kik
    def post(self):
        """
            POST request for submitting a transaction
            Route: Route['kiktransaction']
            Parameters:
                kik: the kik user name (str)
                amount: the amount spent (str)
                sponsor: the name of the sponsor (str)
            Returns:
                status: 200 
                mimetype: application/json
                data: True
        """
        args = parser.parse_args()
        kik = args['kik']
        amount = args['amount']
        sponsor_name = args['sponsor']
        player = Player.query.filter_by(kik=kik).first()
        if player is None:
            # player is found
            raise PlayerNotSubscribed(payload={'details': kik})
        sponsor = Sponsor.query.filter_by(name=sponsor_name).first()
        if sponsor is None:
            # sponsor is not found
            raise SponsorDoesNotExist(payload={'details': sponsor_name})
        teams = find_team_subscribed(kik)
        if len(teams) == 0:
            # kik user is not subscribed to any teams
            raise PlayerNotSubscribed(payload={'details': kik})
        # always give points to team first subscribed to (of current year)
        espy = Espys(team_id=teams[0], sponsor_id=sponsor.id, points=amount, description="Kik transaction")
        DB.session.add(espy)
        DB.session.commit()
        return Response(dumps(espy.id), status=200, mimetype="application/json")
