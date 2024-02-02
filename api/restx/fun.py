from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from datetime import datetime
from .models import get_pagination
from api.extensions import DB
from api.validators import string_validator
from api.model import Fun
from api.authentication import requires_admin
from api.errors import FunDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('count', type=int)
parser.add_argument("page", type=int)
post_parser = reqparse.RequestParser()
post_parser.add_argument('year', type=int, required=True)
post_parser.add_argument('count', type=int, required=True)
HEADERS = [{'header': 'sponsor_name', 'required': True,
            'validator': string_validator}]


fun_api = Namespace(
    "fun",
    description="API for all the League's Fun"
)
fun_payload = fun_api.model('FunPayload', {
    'count': fields.Integer(
        min=0,
        max=10000,
        description="The total count of all the fun"
    ),
})
fun = fun_api.inherit('Fun', fun_payload, {
    'year': fields.Integer(
        min=2016,
        max=datetime.now().year,
        description="The year the fun occurred"
    ),
    'count': fields.Integer(
        min=0,
        max=10000,
        description="The total count of all the fun"
    ),
})
pagination = get_pagination(fun_api)
fun_pagination = fun_api.inherit("FunPagination", pagination, {
    'items': fields.List(fields.Nested(fun))
})


@fun_api.route("/<int:year>", endpoint="rest.fun")
@fun_api.doc(params={"year": "The year the fun occurred"})
class FunAPIX(Resource):

    @fun_api.marshal_with(fun)
    def get(self, year):
        entry = Fun.query.filter(Fun.year == year).first()
        if entry is None:
            raise FunDoesNotExist(payload={'details': year})
        return entry

    @requires_admin
    @fun_api.doc(responses={403: 'Not Authorized', 200: 'Deleted'})
    @fun_api.marshal_with(fun)
    def delete(self, year):

        # delete a single user
        fun_year = Fun.query.filter(Fun.year == year).first()
        if fun_year is None:
            # Sponsor is not in the table
            raise FunDoesNotExist(payload={'details': year})
        fun_json = fun_year.json()
        DB.session.delete(fun_year)
        DB.session.commit()
        handle_table_change(Tables.FUN, item=fun_json)
        return fun_year

    @requires_admin
    @fun_api.doc(responses={403: 'Not Authorized', 200: 'Updated'})
    @fun_api.expect(fun_payload)
    @fun_api.marshal_with(fun)
    def put(self, year):
        fun_year = Fun.query.filter(Fun.year == year).first()
        if fun_year is None:
            raise FunDoesNotExist(payload={'details': year})
        args = parser.parse_args()
        count = args.get('count', None)

        fun_year.update(count=count)
        DB.session.commit()
        handle_table_change(Tables.FUN, item=fun_year.json())
        return fun_year

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


@fun_api.route("", endpoint="rest.funs")
class FunListAPI(Resource):

    @fun_api.marshal_with(fun_pagination)
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Fun.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['fun'])
        return result

    @requires_admin
    @fun_api.doc(responses={403: 'Not Authorized', 200: 'Created'})
    @fun_api.expect(fun)
    @fun_api.marshal_with(fun)
    def post(self):
        args = post_parser.parse_args()
        count = args.get('count', None)
        year = args.get('year', None)
        fun = Fun(year=year, count=count)
        DB.session.add(fun)
        DB.session.commit()
        handle_table_change(Tables.FUN, item=fun.json())
        return fun

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
