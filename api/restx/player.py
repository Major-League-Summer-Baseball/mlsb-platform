from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination
from api.extensions import DB
from api.model import JoinLeagueRequest as TeamRequest, Player, OAuth
from api.authentication import requires_admin
from api.errors import PlayerDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('player_name', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
parser.add_argument('active', type=int)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('player_name', type=str, required=True)
post_parser.add_argument('gender', type=str)
post_parser.add_argument('email', type=str, required=True)
post_parser.add_argument('password', type=str)
post_parser.add_argument("active", type=int)

player_api = Namespace(
    "player",
    description="API for all the League's Players"
)
player_payload = player_api.model('PlayerPayload', {
    'player_name': fields.String(
        description="The name of the player",
    ),
    'gender': fields.String(
        description="The gender of the player",
        default="M",
        enum=['F', 'M', 'T']
    ),
    'active': fields.Boolean(
        description="Whether the player is active in the league or not",
        default=True
    ),
    'email': fields.String(
        description="The email of the player"
    )
})
player = player_api.inherit("Player", player_payload, {
    'player_id': fields.Integer(
        description="The id of the player",
    ),
})
pagination = get_pagination(player_api)
player_pagination = player_api.inherit("PlayerPagination", pagination, {
    'items': fields.List(fields.Nested(player))
})


@player_api.route("/<int:player_id>", endpoint="rest.player")
@player_api.doc(params={"player_id": "The id of the player"})
class PlayerAPIX(Resource):

    @player_api.marshal_with(player)
    def get(self, player_id):
        # expose a single user
        entry = Player.query.get(player_id)
        if entry is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        return entry.json()

    @requires_admin
    @player_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @player_api.marshal_with(player)
    def delete(self, player_id):
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        oauths = OAuth.query.filter(OAuth.player_id == player_id).all()
        for oauth in oauths:
            DB.session.delete(oauth)
        query = TeamRequest.query.filter(TeamRequest.email == player.email)
        for team_request in query.all():
            DB.session.delete(team_request)

        # delete a single user
        DB.session.delete(player)
        DB.session.commit()
        handle_table_change(Tables.PLAYER, item=player.json())
        return player.admin_json()

    @requires_admin
    @player_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @player_api.expect(player_payload)
    @player_api.marshal_with(player)
    def put(self, player_id):
        # update a single user
        player = DB.session.query(Player).get(player_id)
        args = parser.parse_args()
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})

        player_name = args.get("player_name", None)
        gender = args.get("gender", None)
        email = args.get("email", None)
        is_active = args.get("active", True)
        active = is_active == 1 if isinstance(is_active, int) else is_active

        player.update(
            name=player_name,
            gender=gender,
            email=email,
            active=active
        )
        DB.session.commit()
        handle_table_change(Tables.PLAYER, item=player.json())
        return player.admin_json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@player_api.route("", endpoint="rest.players")
class PlayerListAPIX(Resource):

    @player_api.marshal_with(player_pagination)
    def get(self):
        # return a pagination of users
        page = request.args.get('page', 1, type=int)
        pagination = Player.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, url_for('rest.players'))
        return result

    @requires_admin
    @player_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @player_api.expect(player_payload)
    @player_api.marshal_with(player)
    def post(self):
        # create a new user
        args = post_parser.parse_args()

        gender = args.get("gender", "M")
        player_name = args.get("player_name", None)
        email = args.get("email", None)
        is_active = args.get("active", True)
        active = is_active == 1 if isinstance(is_active, int) else is_active
        player = Player(player_name, email, gender, "default", active=active)
        DB.session.add(player)
        DB.session.commit()
        handle_table_change(Tables.PLAYER, item=player.json())
        return player.admin_json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
