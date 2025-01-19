from flask_restx import Resource, Namespace, fields
from flask import request
from .models import get_pagination
from api.cached_items import pull_schedule

schedule_api = Namespace(
    "schedule",
    description="API for all the League's Schedule queries"
)
schedule_payload = schedule_api.model('Schedule', {
    'away_team': fields.String(
        description="The name of the away team",
    ),
    'away_team_id': fields.Integer(
        description="The id of the away team",
    ),
    'date': fields.Date(
        description="The date of the game",
    ),
    'field': fields.String(
        description="The field of the game",
    ),
    'home_team': fields.String(
        description="The name of the home team",
    ),
    'home_team_id': fields.Integer(
        description="The id of the home team",
    ),
    'league_id': fields.Integer(
        description="The id of the league",
    ),
    'score': fields.String(
        description="The score of the game if played",
    ),
    'status': fields.String(
        description="The status of the game",
    ),
    'time': fields.String(
        description="The time of the game (Format: HH-MM)",
        example="12:01"
    ),
})
pagination = get_pagination(schedule_api)
schedule_pagination = schedule_api.inherit("SchedulePagination", pagination, {
    'items': fields.List(fields.Nested(schedule_payload))
})


@schedule_api.route("/<int:year>/<int:league_id>", endpoint="rest.schedule")
@schedule_api.doc(
    params={"year": "The schedule year", "league_id": "The id of the league"}
)
class ScheduleAPIX(Resource):
    @schedule_api.doc(security=[])
    @schedule_api.marshal_with(schedule_pagination)
    def get(self, year, league_id):
        page = request.args.get('page', 1, type=int)
        data = pull_schedule(year, league_id, page=page)
        # running into issue where say this was needed in response
        # just added them for now
        data['year'] = year
        data['league_id'] = league_id
        return data

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'}
