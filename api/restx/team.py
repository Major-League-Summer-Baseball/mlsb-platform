from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from .models import get_pagination
from .player import player
from datetime import date
from api.extensions import DB
from api.model import Team
from api.authentication import requires_admin
from api.errors import TeamDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('color', type=str)
parser.add_argument('league_id', type=int)
parser.add_argument('year', type=int)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('sponsor_id', type=int, required=True)
post_parser.add_argument('color', type=str, required=True)
post_parser.add_argument('league_id', type=int, required=True)
post_parser.add_argument('year', type=int, required=True)

team_api = Namespace(
    "team",
    description="API for all the League's Teams"
)
team_payload = team_api.model("TeamPayload", {
    'color': fields.String(
        description="The color of the team"
    ),
    'sponsor_id': fields.Integer(
        description="The id of the teams's sponsor"
    ),
    'league_id': fields.Integer(
        description="The id of the league the team belongs to"
    ),
    'year': fields.Integer(
        description="The year the team played"
    )
})
team = team_api.inherit("Team", team_payload, {
    'team_id': fields.Integer(
        description="The id of the team"
    ),
    'team_name': fields.String(
        description="The name of the team"
    ),
    'espys': fields.Integer(
        description="The total espys points awarded to the team"
    ),
    'captain': fields.Nested(
        player,
        description="The name of the team"
    ),
})
pagination = get_pagination(team_api)
team_pagination = team_api.inherit("TeamPagination", pagination, {
    'items': fields.List(fields.Nested(team))
})


@team_api.route("/<int:team_id>", endpoint="rest.team")
@team_api.doc(params={"team_id": "The id of the team"})
class TeamAPI(Resource):

    @team_api.marshal_with(team)
    def get(self, team_id):
        # expose a single team
        entry = Team.query.get(team_id)
        if entry is None:
            raise TeamDoesNotExist(payload={'details': team_id})
        return entry.json()

    @requires_admin
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

    @requires_admin
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

        team.update(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year
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

    @team_api.marshal_with(team_pagination)
    def get(self):
        # return a pagination of teams
        page = request.args.get('page', 1, type=int)
        pagination = Team.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['team'])
        return result

    @requires_admin
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

        team = Team(
            color=color,
            sponsor_id=sponsor_id,
            league_id=league_id,
            year=year
        )
        DB.session.add(team)
        DB.session.commit()
        handle_table_change(Tables.TEAM, item=team.json())
        return team.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
