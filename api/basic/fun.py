'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The basic fun API
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import string_validator
from api.model import Fun
from api import DB
from api.authentication import requires_admin
from api.errors import FunDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)
parser.add_argument('count', type=int)
parser.add_argument("page", type=int)
post_parser = reqparse.RequestParser()
post_parser.add_argument('year', type=int, required=True)
post_parser.add_argument('count', type=int, required=True)
HEADERS = [{'header': 'sponsor_name', 'required': True,
            'validator': string_validator}]


class FunAPI(Resource):

    def get(self, year):
        """
            GET request for Fun Object matching given year
            Route: Routes['fun']/<year:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {year:int,
                         count :int
                        }
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # expose a single Sponsor
        entry = Fun.query.filter(Fun.year == year).first()
        if entry is None:
            raise FunDoesNotExist(payload={'details': year})
        response = Response(dumps(entry.json()),
                            status=200, mimetype="application/json")
        return response

    @requires_admin
    def delete(self, year):
        """
            DELETE request for Fun
            Route: Routes['fun']/<year:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data: None
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # delete a single user
        fun_year = Fun.query.filter(Fun.year == year).first()
        if fun_year is None:
            # Sponsor is not in the table
            raise FunDoesNotExist(payload={'details': year})
        DB.session.delete(fun_year)
        DB.session.commit()
        return Response(dumps(None), status=200, mimetype="application/json")

    @requires_admin
    def put(self, year):
        """
            PUT request for Sponsor
            Route: Routes['fun']/<year:int>
            Parameters :
                count: The number of fun (int)
            Returns:
                if found and successful
                    status: 200
                    mimetype: application/json
                    data: None
                if found but not successful
                    status: 409
                    mimetype: application/json
                    data: None
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # update a single user
        fun_year = Fun.query.filter(Fun.year == year).first()
        count = None
        if fun_year is None:
            raise FunDoesNotExist(payload={'details': year})
        args = parser.parse_args()
        if args['count']:
            count = args['count']
        fun_year.update(count=count)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class FunListAPI(Resource):

    def get(self):
        """
            GET request for Fun List
            Route: Routes['fun']
            Parameters :

            Returns:
                status: 200
                mimetype: application/json
                data:
                    Sponsors: [{year: int, count:int
                                },{...}
                            ]
        """
        # return a pagination of sponsors
        page = request.args.get('page', 1, type=int)
        pagination = Fun.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['fun'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Sponsor List
            Route: Routes['fun']
            Parameters :
                year: The Sponsor's name (string)
                count: A link to sponsors website (string)
                description: a description of the sponsor (string)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    sponsor_id: the create sponsor_id
                else
                    status: 409
                    mimetype: application/json
                    data: the create sponsor_id (int)
        """
        # create a new user
        args = post_parser.parse_args()
        count = None
        year = None
        if args['count']:
            count = args['count']
        if args['year']:
            year = args['year']
        fun = Fun(year=year,
                  count=count)
        DB.session.add(fun)
        DB.session.commit()
        fun_id = fun.year
        return Response(dumps(fun_id), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
