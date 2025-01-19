from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination, team, team_payload
from datetime import date
from api.extensions import DB
from api.model import Team
from api.authentication import require_to_be_convenor
from api.errors import TeamDoesNotExist
from api.variables import PAGE_SIZE
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables


parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('color', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('year', type=int)
parser.add_argument('image_id', type=int)

post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('sponsor_id', type=int, required=True)
post_parser.add_argument('color', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
post_parser.add_argument('year', type=int, required=True)
post_parser.add_argument('image_id', type=int)

lookup_parser = reqparse.RequestParser(bundle_errors=True)
lookup_parser.add_argument('sponsor_id', type=int)
lookup_parser.add_argument('color', type=str)
lookup_parser.add_argument('league_id', type=int)
lookup_parser.add_argument('year', type=int)


team_api = Namespace(
    "team",
    description="API for all the League's Teams"
)
team_lookup = team_api.model("TeamLookup", {
    'sponsor_id': fields.Integer(
        description="Filter by sponsors of the team",
        required=False
    ),
    'year': fields.Integer(
        description="Filter by year of the team",
        required=False
    ),
    'team_id': fields.Integer(
        description="Filter by year of the team",
        required=False
    ),
    'color': fields.String(
        description="Filter by color of the team",
        required=False
    )
})
pagination = get_pagination(team_api)
team_pagination = team_api.inherit("TeamPagination", pagination, {
    'items': fields.List(fields.Nested(team))
})


@team_api.route("/<int:team_id>", endpoint="rest.team")
@team_api.doc(params={"team_id": "The id of the team"})
class TeamAPI(Resource):
    @team_api.doc(security=[])
    @team_api.marshal_with(team)
    def get(self, team_id):
        # expose a single team
        entry = Team.query.get(team_id)
        if entry is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        return entry.json()

    @require_to_be_convenor
    @team_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @team_api.marshal_with(team)
    def delete(self, team_id):
        # delete a single team
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        team_json = team.json()
        DB.session.delete(team)
        DB.session.commit()
        handle_table_change(Tables.TEAM, item=team_json)
        return team_json

    @require_to_be_convenor
    @team_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @team_api.expect(team_payload)
    @team_api.marshal_with(team)
    def put(self, team_id):
        # update a single user
        team = Team.query.get(team_id)
        if team is None:
            raise TeamDoesNotExist(payload={'details': team_id})

        args = parser.parse_args()
        color = args.get('color', None)
        sponsor_id = args.get('sponsor_id', None)
        league_id = args.get('league_id', None)
        year = args.get('year', None)
        image_id = args.get('image_id', None)

        team.update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year,
            image_id=image_id
        )
        DB.session.commit()
        handle_table_change(Tables.TEAM, item=team.json())
        return team.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@team_api.route("", endpoint="rest.teams")
class TeamListAPI(Resource):
    @team_api.doc(security=[])
    @team_api.marshal_with(team_pagination)
    def get(self):
        # return a pagination of teams
        page = request.args.get('page', 1, type=int)
        pagination = Team.query.paginate(
            page=page, per_page=PAGE_SIZE, error_out=False
        )
        result = pagination_response(pagination, url_for('rest.teams'))
        return result

    @require_to_be_convenor
    @team_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @team_api.expect(team_payload)
    @team_api.marshal_with(team)
    def post(self):
        # create a new user
        args = post_parser.parse_args()
        args = parser.parse_args()
        color = args.get('color', None)
        sponsor_id = args.get('sponsor_id', None)
        league_id = args.get('league_id', None)
        year = args.get('year', date.today().year)
        image_id = args.get('image_id', None)

        team = Team(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year,
            image_id=image_id
        )
        DB.session.add(team)
        DB.session.commit()
        handle_table_change(Tables.TEAM, item=team.json())
        return team.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@team_api.route("lookup", endpoint="rest.teamlookup")
class TeamLookupAPI(Resource):
    @team_api.expect(team_lookup)
    @team_api.marshal_list_with(team)
    def post(self):
        args = lookup_parser.parse_args()
        color = args.get('color', None)
        sponsor_id = args.get('sponsor_id', None)
        league_id = args.get('league_id', None)
        year = args.get('year', None)
        team_query = Team.query

        if league_id is not None:
            team_query = team_query.filter(Team.league_id == league_id)
        if year is not None:
            team_query = team_query.filter(Team.year == year)
        if sponsor_id is not None:
            team_query = team_query.filter(Team.sponsor_id == sponsor_id)
        if color is not None:
            team_query = team_query.filter(Team.color.contains(color))

        teams = team_query.all()
        return [team.json() for team in teams]

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
