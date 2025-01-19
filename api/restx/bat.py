from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination
from api.extensions import DB
from api.model import Bat
from api.authentication import require_to_be_convenor
from api.errors import BatDoesNotExist
from api.variables import PAGE_SIZE, BATS
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('player_id', type=int)
parser.add_argument('rbi', type=int)
parser.add_argument('game_id', type=int)
parser.add_argument('hit', type=str)
parser.add_argument('inning', type=int)
parser.add_argument('team_id', type=str)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('player_id', type=int, required=True)
post_parser.add_argument('rbi', type=int)
post_parser.add_argument('game_id', type=int, required=True)
post_parser.add_argument('hit', type=str, required=True)
post_parser.add_argument('inning', type=int)
post_parser.add_argument('team_id', type=str, required=True)

bat_api = Namespace(
    "bat",
    description="API for all the League's bats"
)
bat_payload = bat_api.model('BatPayload', {
    'game_id': fields.Integer(
        description="The id of the game",
    ),
    'player_id': fields.Integer(
        description="The id of the player",
    ),
    'team_id': fields.Integer(
        description="The id of the team",
    ),
    'hit': fields.String(
        description="The id of the division",
        enum=BATS
    ),
    'rbi': fields.Integer(
        min=0,
        max=4,
        description="The number of runs batter in",

    ),
    'inning': fields.Integer(
        min=1,
        description="The inning of the bat",
    ),
})
bat = bat_api.inherit("Bat", bat_payload, {
    'bat_id': fields.Integer(
        description="The id of the bat",
    ),
    'team': fields.String(
        description="The name of the team"
    ),
    'player': fields.String(
        description="The name of the player"
    ),
})
pagination = get_pagination(bat_api)
bat_pagination = bat_api.inherit("BatPagination", pagination, {
    'items': fields.List(fields.Nested(bat))
})


@bat_api.route("/<int:bat_id>", endpoint="rest.bat")
@bat_api.doc(params={"bat_id": "The id of the bat"})
class BatAPI(Resource):

    @bat_api.doc(security=[])
    @bat_api.marshal_with(bat)
    def get(self, bat_id):
        entry = Bat.query.get(bat_id)
        if entry is None:
            raise BatDoesNotExist(payload={'details': bat_id})
        return entry.json()

    @require_to_be_convenor
    @bat_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @bat_api.marshal_with(bat)
    def delete(self, bat_id):
        bat = Bat.query.get(bat_id)
        if bat is None:
            raise BatDoesNotExist(payload={'details': bat_id})
        # delete a single bat
        DB.session.delete(bat)
        DB.session.commit()
        handle_table_change(Tables.BAT, item=bat.json())
        return bat.json()

    @require_to_be_convenor
    @bat_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @bat_api.expect(bat_payload)
    @bat_api.marshal_with(bat)
    def put(self, bat_id):
        # update a single bat
        bat = Bat.query.get(bat_id)
        if bat is None:
            raise BatDoesNotExist(payload={'details': bat_id})

        args = parser.parse_args()
        game_id = args.get('game_id', None)
        player_id = args.get('player_id', None)
        team_id = args.get('team_id', None)
        rbi = args.get('rbi', None)
        hit = args.get('hit', None)
        inning = args.get('inning', None)

        bat.update(
            player_id=player_id,
            team_id=team_id,
            game_id=game_id,
            rbi=rbi,
            hit=hit,
            inning=inning
        )
        DB.session.commit()
        handle_table_change(Tables.BAT, item=bat.json())
        return bat.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@bat_api.route("", endpoint="rest.bats")
class BatListAPI(Resource):

    @bat_api.doc(security=[])
    @bat_api.marshal_with(bat_pagination)
    def get(self):
        #  return a pagination of bats
        page = request.args.get('page', 1, type=int)
        pagination = Bat.query.paginate(
            page=page, per_page=PAGE_SIZE, error_out=False
        )
        return pagination_response(pagination, url_for('rest.bats'))

    @require_to_be_convenor
    @bat_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @bat_api.expect(bat_payload)
    @bat_api.marshal_with(bat)
    def post(self):
        # create a new bat
        args = post_parser.parse_args()
        game_id = args.get('game_id', None)
        player_id = args.get('player_id', None)
        team_id = args.get('team_id', None)
        rbi = args.get('rbi', 0)
        hit = args.get('hit', None)

        inning = args.get('inning', 1)
        bat = Bat(
            player_id,
            team_id,
            game_id,
            hit,
            # just assume some first inning
            inning=inning if inning is not None else 1,
            rbi=rbi
        )
        DB.session.add(bat)
        DB.session.commit()
        handle_table_change(Tables.BAT, item=bat.json())
        return bat.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
