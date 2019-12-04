'''
@author: Dallas Fraser
@date: 2015-08-25
@organization: MLSB API
@summary: The basic league API
'''
from flask_restful import Resource, reqparse
from flask import Response
from api.model import League
from json import dumps
from api import DB
from api.authentication import requires_admin
from api.errors import LeagueDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('league_name', type=str)
post_parser = reqparse.RequestParser()
post_parser.add_argument('league_name', type=str, required=True)


class LeagueAPI(Resource):
    def get(self, league_id):
        """
            GET request for League Object matching given league_id
            Route: Route['league']/<league_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data: {league_id:int, league_name:string}
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # expose a single League
        entry = League.query.get(league_id)
        if entry is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, league_id):
        """
            DELETE request for League
            Route: Route['league']/<league_id: int>
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
        league = League.query.get(league_id)
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        DB.session.delete(league)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, league_id):
        """
            PUT request for league
            Route: Route['league']/<league_id: int>
            Parameters :
                league_name: The league's name (string)
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
        league = League.query.get(league_id)
        league_name = None
        if league is None:
            raise LeagueDoesNotExist(payload={'details': league_id})
        if args['league_name']:
            league_name = args['league_name']
        league.update(league_name)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class LeagueListAPI(Resource):
    def get(self):
        """
            GET request for League List
            Route: Route['league']
            Parameters :
                league_name: The league's name (string)
            Returns:
                status: 200
                mimetype: application/json
                data:
                    tournaments: [{league_id:int,
                                   league_name:string,
                                  },{...}
                            ]
        """
        # return a pagination of leagues
        page = request.args.get('page', 1, type=int)
        pagination = League.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['league'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for League List
            Route: Route['league']
            Parameters :
                league_name: The league's name (string)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created user league id (int)
                if missing required parameter
                    status: 400
                    mimetype: application/json
                    data: the created user league id (int)
                if invalid parameter
                    status: IFSC
                    mimetype: application/json
                    data: the created user league id (int)
        """
        # create a new user
        args = post_parser.parse_args()
        league_name = None
        if args['league_name']:
            league_name = args['league_name']
        league = League(league_name)
        DB.session.add(league)
        DB.session.commit()
        result = league.id
        return Response(dumps(result), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
