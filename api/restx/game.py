from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from .models import get_pagination
from api.extensions import DB
from api.variables import FIELDS
from api.model import Game
from api.authentication import requires_admin
from api.errors import GameDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('home_team_id', type=int)
parser.add_argument('away_team_id', type=int)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('division_id', type=int)
parser.add_argument('status', type=str)
parser.add_argument('field', type=str)

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('home_team_id', type=int, required=True)
post_parser.add_argument('away_team_id', type=int, required=True)
post_parser.add_argument('date', type=str, required=True)
post_parser.add_argument('time', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
post_parser.add_argument('division_id', type=int, required=True)
post_parser.add_argument('status', type=str)
post_parser.add_argument('field', type=str)


game_api = Namespace(
    "game",
    description="API for all the League's games"
)
game_payload = game_api.model('GamePayload', {
    'home_team_id': fields.Integer(
        description="The id of the home team",
    ),
    'away_team_id': fields.Integer(
        description="The id of the away team",
    ),
    'league_id': fields.Integer(
        description="The id of the league",
    ),
    'division_id': fields.Integer(
        description="The id of the division",
    ),
    'status': fields.String(
        description="The status of the game",
    ),
    'field': fields.String(
        description="The status of the game",
        enum=FIELDS
    ),
    'date': fields.Date(
        description="The date of the espys",
    ),
    'time': fields.String(
        description="The time of the espys (Format: HH-MM)",
        example="12:01"
    ),
})
game = game_api.inherit("Game", game_payload, {
    'game_id': fields.Integer(
        description="The id of the game",
    ),
    'home_team': fields.String(
        description="The name of the home team"
    ),
    'away_team': fields.String(
        description="The name of away team"
    ),
})
pagination = get_pagination(game_api)
game_pagination = game_api.inherit("GamePagination", pagination, {
    'items': fields.List(fields.Nested(game))
})


@game_api.route("/<int:game_id>", endpoint="rest.game")
@game_api.doc(params={"game_id": "The id of the game"})
class GameAPI(Resource):

    @game_api.marshal_with(game)
    def get(self, game_id):
        # expose a single game
        entry = Game.query.get(game_id)
        if entry is None:
            raise GameDoesNotExist(payload={'details': game_id})
        return entry.json()

    @requires_admin
    @game_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @game_api.marshal_with(game)
    def delete(self, game_id):
        game = Game.query.get(game_id)
        if game is None:
            raise GameDoesNotExist(payload={'details': game_id})
        DB.session.delete(game)
        DB.session.commit()
        handle_table_change(Tables.GAME, item=game.json())
        return game.json()

    @requires_admin
    @game_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @game_api.expect(game_payload)
    @game_api.marshal_with(game)
    def put(self, game_id):
        game = Game.query.get(game_id)
        if game is None:
            raise GameDoesNotExist(payload={'details': game_id})

        args = parser.parse_args()
        game.update(
            date=args.get('date', None),
            time=args.get('time', None),
            home_team_id=args.get('home_team_id', None),
            away_team_id=args.get('away_team_id', None),
            league_id=args.get('league_id', None),
            division_id=args.get('division_id', None),
            status=args.get('status', None),
            field=args.get('field', None)
        )
        DB.session.commit()
        handle_table_change(Tables.GAME, item=game.json())
        return game.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@game_api.route("", endpoint="rest.games")
class GameListAPI(Resource):

    @game_api.marshal_with(game_pagination)
    def get(self):
        # return a pagination of games
        page = request.args.get('page', 1, type=int)
        pagination = Game.query.paginate(page, PAGE_SIZE, False)
        return pagination_response(pagination, Routes['game'])

    @requires_admin
    @game_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @game_api.expect(game_payload)
    @game_api.marshal_with(game)
    def post(self):
        # create a new game
        args = post_parser.parse_args()
        date = None
        time = None
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        status = args.get('status', '')
        field = args.get('field', '')
        game = Game(
            date,
            time,
            args.get('home_team_id'),
            args.get('away_team_id'),
            args.get('league_id'),
            args.get('division_id'),
            status=status if status is not None else '',
            field=field if field is not None else ''
        )
        DB.session.add(game)
        DB.session.commit()
        handle_table_change(Tables.GAME, item=game.json())
        return game.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
