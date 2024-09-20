from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination
from api.extensions import DB
from api.model import League
from api.authentication import require_to_be_convenor
from api.errors import LeagueDoesNotExist
from api.variables import PAGE_SIZE
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables

parser = reqparse.RequestParser()
parser.add_argument('league_name', type=str)
post_parser = reqparse.RequestParser()
post_parser.add_argument('league_name', type=str, required=True)


league_api = Namespace(
    "league",
    description="API for all the Leagues"
)
league_payload = league_api.model('LeaguePayload', {
    'league_name': fields.String(
        description="The name of the league",
    ),
})
league = league_api.inherit("League", league_payload, {
    'league_id': fields.Integer(
        description="The id of the league",
    ),
})
pagination = get_pagination(league_api)
league_pagination = league_api.inherit("LeaguePagination", pagination, {
    'items': fields.List(fields.Nested(league))
})


@league_api.route("/<int:league_id>", endpoint="rest.league")
@league_api.doc(params={"league_id": "The id of the league"})
class LeagueAPI(Resource):
    @league_api.doc(security=[])
    @league_api.marshal_with(league)
    def get(self, league_id):
        # expose a single League
        entry = League.query.get(league_id)
        if entry is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        return entry.json()

    @require_to_be_convenor
    @league_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @league_api.marshal_with(league)
    def delete(self, league_id):
        # delete a single user
        league = League.query.get(league_id)
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        DB.session.delete(league)
        DB.session.commit()
        handle_table_change(Tables.LEAGUE, item=league.json())
        return league.json()

    @require_to_be_convenor
    @league_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @league_api.expect(league_payload)
    @league_api.marshal_with(league)
    def put(self, league_id):
        # update a single user
        league = League.query.get(league_id)
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league_id})

        args = parser.parse_args()
        league_name = args.get('league_name', None)
        league.update(league_name)
        DB.session.commit()
        handle_table_change(Tables.LEAGUE, item=league.json())
        return league.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@league_api.route("", endpoint="rest.leagues")
class LeagueListAPI(Resource):
    @league_api.doc(security=[])
    @league_api.marshal_with(league_pagination)
    def get(self):
        # return a pagination of leagues
        page = request.args.get('page', 1, type=int)
        pagination = League.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, url_for('rest.leagues'))
        return result

    @require_to_be_convenor
    @league_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @league_api.expect(league_payload)
    @league_api.marshal_with(league)
    def post(self):
        # create a new user
        args = post_parser.parse_args()
        league_name = args.get('league_name', None)

        league = League(league_name)
        DB.session.add(league)
        DB.session.commit()
        handle_table_change(Tables.LEAGUE, item=league.json())
        return league.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
