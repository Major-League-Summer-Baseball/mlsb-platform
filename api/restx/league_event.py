from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from .models import get_pagination
from api.extensions import DB
from api.model import LeagueEvent
from api.authentication import requires_admin
from api.errors import LeagueEventDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('active', type=str)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('description', type=str, required=True)
post_parser.add_argument('active', type=str)

league_event_api = Namespace(
    "league_event",
    description="API for all the League's Events"
)
league_event_payload = league_event_api.model('LeagueEventPayload', {
    'name': fields.String(
        description="The name of the event",
    ),
    'description': fields.String(
        description="The description of the event",
    ),
    'active': fields.Boolean(
        description="Whether the event is active for the league"
    )
})
league_event = league_event_api.inherit("LeagueEvent", league_event_payload, {
    'league_event_id': fields.Integer(
        description="The id of the league event",
    ),
})
pagination = get_pagination(league_event_api)
league_event_pagination = league_event_api.inherit(
    "LeagueEventPagination",
    pagination,
    {'items': fields.List(fields.Nested(league_event))}
)


def convert_active(active: str) -> bool:
    """Converts active from None||1||0 to a boolean"""
    if active is None:
        return None
    return True if active == "1" else False


@league_event_api.route("/<int:league_event_id>", endpoint="rest.league_event")
@league_event_api.doc(params={"league_event_id": "The id of the league event"})
class LeagueEventAPI(Resource):

    @league_event_api.marshal_with(league_event)
    def get(self, league_event_id):
        entry = LeagueEvent.query.get(league_event_id)
        if entry is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})
        return entry.json()

    @requires_admin
    @league_event_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @league_event_api.marshal_with(league_event)
    def delete(self, league_event_id):
        league_event = LeagueEvent.query.get(league_event_id)
        if league_event is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})

        DB.session.delete(league_event)
        DB.session.commit()
        return league_event.json()

    @requires_admin
    @league_event_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @league_event_api.expect(league_event_payload)
    @league_event_api.marshal_with(league_event)
    def put(self, league_event_id):
        league_event = LeagueEvent.query.get(league_event_id)
        if league_event is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})

        args = parser.parse_args()
        description = args.get('description', None)
        name = args.get('name', None)
        active = convert_active(args.get('active', None))

        league_event.update(
            name=name,
            description=description,
            active=active
        )
        DB.session.commit()
        return league_event.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@league_event_api.route("", endpoint="rest.league_events")
class LeagueEventListAPI(Resource):

    @league_event_api.marshal_with(league_event_pagination)
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = LeagueEvent.query.paginate(page, PAGE_SIZE, False)
        return pagination_response(pagination, Routes['league_event'])

    @requires_admin
    @league_event_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @league_event_api.expect(league_event_payload)
    @league_event_api.marshal_with(league_event)
    def post(self):
        args = post_parser.parse_args()
        description = args.get('description')
        name = args.get('name')
        active = convert_active(args.get('active', "1"))
        active = active if active is not None else True

        league_event = LeagueEvent(name, description, active=active)
        DB.session.add(league_event)
        DB.session.commit()
        return league_event.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
