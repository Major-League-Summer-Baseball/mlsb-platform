from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import Division
from api.extensions import DB
from api.authentication import requires_admin
from api.errors import DivisionDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('division_name', type=str)
parser.add_argument('division_shortname', type=str)
post_parser = reqparse.RequestParser()
post_parser.add_argument('division_name', type=str, required=True)
post_parser.add_argument('division_shortname', type=str)


class DivisionAPI(Resource):
    def get(self, division_id):
        """
            GET request for Division Object matching given division_id
            Route: Route['division']/<division_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data: {
                        division_id:int,
                        division_name:string,
                        division_shortname:string
                    }
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # expose a single Division
        entry = Division.query.get(division_id)
        if entry is None:
            raise DivisionDoesNotExist(payload={'details': division_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, division_id):
        """
            DELETE request for Division
            Route: Route['division']/<division_id: int>
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
        # delete a single division
        division = Division.query.get(division_id)
        if division is None:
            raise DivisionDoesNotExist(payload={'details': division_id})
        DB.session.delete(division)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, division_id):
        """
            PUT request for Division
            Route: Route['division']/<division_id: int>
            Parameters :
                division_name: The division's name (string)
                division_shortname: The shortened division's name (string)
            Returns:
                if found and successful
                    status: 200
                    mimetype: application/json
                    data: None
                if found but not successful
                    status: IFSC
                    mimetype: application/json
                    data: None
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # update a single user
        args = parser.parse_args()
        division = Division.query.get(division_id)
        name = None
        shortname = None
        if division is None:
            raise DivisionDoesNotExist(payload={'details': division_id})
        if args['division_name']:
            name = args['division_name']
        if args['division_shortname']:
            shortname = args['division_shortname']
        division.update(name=name, shortname=shortname)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class DivisionListAPI(Resource):
    def get(self):
        """
            GET request for Division List
            Route: Route['division']
            Returns:
                status: 200
                mimetype: application/json
                Paginated list of division objects
        """
        # return a pagination of Divisions
        page = request.args.get('page', 1, type=int)
        pagination = Division.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['division'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Division
            Route: Route['division']
            Parameters :
                division_name: The Division's name (string)
                division_shortname: The shortened version of
                    Division's name (string)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created user division id (int)
                if missing required parameter
                    status: 400
                    mimetype: application/json
                    data: missing parameter
                if invalid parameter
                    status: IFSC
                    mimetype: application/json
                    data: the invalid field
        """
        # create a new user
        args = post_parser.parse_args()
        name = None
        shortname = None
        if args['division_name']:
            name = args['division_name']
        if args['division_shortname']:
            shortname = args['division_shortname']
        division = Division(name, shortname=shortname)
        DB.session.add(division)
        DB.session.commit()
        result = division.id
        return Response(dumps(result), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
