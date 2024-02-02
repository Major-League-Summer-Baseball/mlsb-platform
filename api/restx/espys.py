from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from .models import get_pagination
from api.extensions import DB
from api.model import Espys
from api.authentication import requires_admin
from api.errors import EspysDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('team_id', type=int)
parser.add_argument('description', type=str)
parser.add_argument('points', type=str)
parser.add_argument('receipt', type=str)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('sponsor_id', type=int)
post_parser.add_argument('team_id', type=int, required=True)
post_parser.add_argument('description', type=str)
post_parser.add_argument('points', type=str, required=True)
post_parser.add_argument('receipt', type=str)
post_parser.add_argument('date', type=str)
post_parser.add_argument('time', type=str)


espys_api = Namespace(
    "espys",
    description="API for all the League's Espys"
)
espys_payload = espys_api.model('EspysPayload', {
    'sponsor_id': fields.Integer(
        description="The id of the sponsor associated with espy points",
    ),
    'team_id': fields.Integer(
        description="The id of the team getting the espy points",
    ),
    'description': fields.String(
        description="The description of why points were awarded",
    ),
    'points': fields.Float(
        description="The number of points awarded",
    ),
    'receipt': fields.String(
        description="The receipt of the espys",
    ),
    'date': fields.Date(
        description="The date of the espys",
    ),
    'time': fields.String(
        description="The time of the espys (Format: HH-MM)",
        example="12:01"
    ),
})
espys = espys_api.inherit("Espys", espys_payload, {
    'espy_id': fields.Integer(
        description="The id of the espy points",
    ),
})
pagination = get_pagination(espys_api)
espys_pagination = espys_api.inherit("EspysPagination", pagination, {
    'items': fields.List(fields.Nested(espys))
})


@espys_api.route("<int:espy_id>", endpoint="rest.espy")
@espys_api.doc(params={"espy_id": "The id of the espy points"})
class EspyAPI(Resource):

    @espys_api.marshal_with(espys)
    def get(self, espy_id):
        # expose a single team
        entry = Espys.query.get(espy_id)
        if entry is None:
            raise EspysDoesNotExist(payload={'details': espy_id})
        return entry.json()

    @requires_admin
    @espys_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @espys_api.marshal_with(espys, code=200)
    def delete(self, espy_id):
        espy = Espys.query.get(espy_id)
        if espy is None:
            raise EspysDoesNotExist(payload={'details': espy_id})
        # delete a single espy
        DB.session.delete(espy)
        DB.session.commit()
        handle_table_change(Tables.ESPYS, item=espy.json())
        return espy.json()

    @requires_admin
    @espys_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @espys_api.expect(espys_payload)
    @espys_api.marshal_with(espys, code=200)
    def put(self, espy_id):
        # update a single user
        espy = Espys.query.get(espy_id)
        if espy is None:
            raise EspysDoesNotExist(payload={'details': espy_id})

        args = parser.parse_args()
        description = args.get("description", None)
        sponsor_id = args.get("sponsor_id", None)
        team_id = args.get("team_id", None)
        points = args.get("points", None)
        receipt = args.get("receipt", None)
        date = None
        time = None
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']

        espy.update(
            sponsor_id=sponsor_id,
            team_id=team_id,
            description=description,
            points=points,
            receipt=receipt,
            date=date,
            time=time
        )
        DB.session.commit()
        handle_table_change(Tables.ESPYS, item=espy.json())
        return espy.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@espys_api.route("", endpoint="rest.espys")
class EspyListAPI(Resource):

    @espys_api.marshal_with(espys_pagination)
    def get(self):
        # return a pagination of teams
        page = request.args.get('page', 1, type=int)
        pagination = Espys.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['espy'])
        return result

    @requires_admin
    @espys_api.doc(responses={403: 'Not Authorized', 201: 'Created'})
    @espys_api.expect(espys_payload)
    @espys_api.marshal_with(espys, code=201)
    def post(self):
        # create a new user
        args = post_parser.parse_args()
        description = args.get("description", None)
        sponsor_id = args.get("sponsor_id", None)
        team_id = args.get("team_id", None)
        points = args.get("points", None)
        receipt = args.get("receipt", None)
        date = None
        time = None
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']

        espy = Espys(
            sponsor_id=sponsor_id,
            team_id=team_id,
            description=description,
            points=points,
            receipt=receipt,
            date=date,
            time=time
        )
        DB.session.add(espy)
        DB.session.commit()
        handle_table_change(Tables.ESPYS, item=espy.json())
        return espy.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
