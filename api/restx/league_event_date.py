from flask_restx import Resource, reqparse, Namespace, fields
from flask import request, url_for
from .models import get_pagination
from api.extensions import DB
from api.model import LeagueEventDate
from api.authentication import require_to_be_convenor
from api.errors import LeagueEventDateDoesNotExist
from api.variables import PAGE_SIZE
from api.helper import pagination_response

parser = reqparse.RequestParser()
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_event_id', type=int)
parser.add_argument('image_id', type=int)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('date', type=str, required=True)
post_parser.add_argument('time', type=str, required=True)
post_parser.add_argument('league_event_id', type=int, required=True)
post_parser.add_argument('image_id', type=int)

league_event_date_api = Namespace(
    "league_event_date",
    description="API for all the League's Event Dates"
)
league_event_date_payload = league_event_date_api.model(
    'LeagueEventDatePayload',
    {
        'league_event_id': fields.Integer(
            description="The id of the league event",
        ),
        'date': fields.Date(
            description="The date of the league event",
        ),
        'time': fields.String(
            description="The time of the league event (Format: HH-MM)",
            example="12:01"
        ),
        'image_id': fields.Integer(
            description="The image for the event for given date",
        ),
    }
)
league_event_date = league_event_date_api.inherit(
    "LeagueEventDate",
    league_event_date_payload,
    {
        'league_event_date_id': fields.Integer(
            description="The id of the league event date",
        ),
    }
)
pagination = get_pagination(league_event_date_api)
league_event_date_pagination = league_event_date_api.inherit(
    "LeagueEventDatePagination",
    pagination,
    {'items': fields.List(fields.Nested(league_event_date))}
)


@league_event_date_api.route(
    "/<int:league_event_date_id>",
    endpoint="rest.league_event_date"
)
@league_event_date_api.doc(
    params={"league_event_date_id": "The id of the league event date"}
)
class LeagueEventDateAPI(Resource):
    @league_event_date_api.doc(security=[])
    @league_event_date_api.marshal_with(league_event_date)
    def get(self, league_event_date_id):
        entry = LeagueEventDate.query.get(league_event_date_id)
        if entry is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)
        return entry.json()

    @require_to_be_convenor
    @league_event_date_api.doc(
        responses={403: 'Not Authorized', 200: 'Deleted'}
    )
    @league_event_date_api.marshal_with(league_event_date)
    def delete(self, league_event_date_id):
        league_event_date = LeagueEventDate.query.get(league_event_date_id)
        if league_event_date is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)

        DB.session.delete(league_event_date)
        DB.session.commit()
        return league_event_date.json()

    @require_to_be_convenor
    @league_event_date_api.doc(
        responses={403: 'Not Authorized', 200: 'Updated'}
    )
    @league_event_date_api.expect(league_event_date_payload)
    @league_event_date_api.marshal_with(league_event_date)
    def put(self, league_event_date_id):
        league_event_date = LeagueEventDate.query.get(league_event_date_id)
        if league_event_date is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)

        args = parser.parse_args()
        league_event_id = args.get('league_event_id', None)
        image_id = args.get('image_id', None)
        date = args.get('date', None)
        time = args.get('time', None)

        league_event_date.update(
            league_event_id=league_event_id,
            date=date,
            time=time,
            image_id=image_id,
        )
        DB.session.commit()
        return league_event_date.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@league_event_date_api.route("", endpoint="rest.league_event_dates")
class LeagueEventDateListAPI(Resource):
    @league_event_date_api.doc(security=[])
    @league_event_date_api.marshal_with(league_event_date_pagination)
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = LeagueEventDate.query.paginate(
            page=page, per_page=PAGE_SIZE, error_out=False
        )
        return pagination_response(
            pagination, url_for('rest.league_event_dates')
        )

    @require_to_be_convenor
    @league_event_date_api.doc(
        responses={403: 'Not Authorized', 200: 'Created'}
    )
    @league_event_date_api.expect(league_event_date_payload)
    @league_event_date_api.marshal_with(league_event_date)
    def post(self):
        args = post_parser.parse_args()

        league_event_id = args.get('league_event_id', None)
        date = args.get('date', None)
        time = args.get('time', None)
        image_id = args.get('image_id', None)

        league_event_date = LeagueEventDate(
            date, time, league_event_id, image_id=image_id
        )
        DB.session.add(league_event_date)
        DB.session.commit()
        return league_event_date.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
