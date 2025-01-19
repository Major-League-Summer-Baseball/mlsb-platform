from flask_restx import Resource, reqparse, Namespace, fields
from .models import get_pagination
from api.model import Division
from api.extensions import DB
from api.authentication import require_to_be_convenor
from api.errors import DivisionDoesNotExist
from api.variables import PAGE_SIZE
from api.helper import pagination_response
from flask import request, url_for
parser = reqparse.RequestParser()
parser.add_argument('division_name', type=str)
parser.add_argument('division_shortname', type=str)
post_parser = reqparse.RequestParser()
post_parser.add_argument('division_name', type=str, required=True)
post_parser.add_argument('division_shortname', type=str)

division_api = Namespace(
    "division",
    description="API for all the League's division"
)
division_payload = division_api.model('DivisionPayload', {
    'division_name': fields.String(
        description="The name of the division",
    ),
    'division_shortname': fields.String(
        description="The shortened name of the division",
        required=False
    ),
})
division = division_api.inherit("Division", division_payload, {
    'division_id': fields.Integer(
        description="The id of the division",
    ),
})
pagination = get_pagination(division_api)
division_pagination = division_api.inherit("DivisionPagination", pagination, {
    'items': fields.List(fields.Nested(division))
})


@division_api.route("/<int:division_id>", endpoint="rest.division")
@division_api.doc(params={"division_id": "The id of the division"})
class DivisionAPI(Resource):
    @division_api.doc(security=[])
    @division_api.marshal_with(division)
    def get(self, division_id):
        # expose a single Division
        entry = Division.query.get(division_id)
        if entry is None:
            raise DivisionDoesNotExist(payload={'details': division_id})
        return entry.json()

    @require_to_be_convenor
    @division_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @division_api.marshal_with(division)
    def delete(self, division_id):
        # delete a single division
        division = Division.query.get(division_id)
        if division is None:
            raise DivisionDoesNotExist(payload={'details': division_id})
        DB.session.delete(division)
        DB.session.commit()
        return division.json()

    @require_to_be_convenor
    @division_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @division_api.expect(division_payload)
    @division_api.marshal_with(division)
    def put(self, division_id):
        # update a single user
        division = Division.query.get(division_id)
        if division is None:
            raise DivisionDoesNotExist(payload={'details': division_id})

        args = parser.parse_args()
        name = args.get('division_name', None)
        shortname = args.get('division_shortname', None)

        division.update(name=name, shortname=shortname)
        DB.session.commit()
        return division.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@division_api.route("", endpoint="rest.divisions")
class DivisionListAPI(Resource):
    @division_api.doc(security=[])
    @division_api.marshal_with(division_pagination)
    def get(self):
        # return a pagination of Divisions
        page = request.args.get('page', 1, type=int)
        pagination = Division.query.paginate(
            page=page, per_page=PAGE_SIZE, error_out=False
        )
        result = pagination_response(pagination, url_for('rest.divisions'))
        return result

    @require_to_be_convenor
    @division_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @division_api.expect(division_payload)
    @division_api.marshal_with(division)
    def post(self):
        # create a new user
        args = post_parser.parse_args()
        name = args.get('division_name', None)
        shortname = args.get('division_shortname', None)

        division = Division(name, shortname=shortname)
        DB.session.add(division)
        DB.session.commit()
        return division.json()

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
