'''
@author: Dalton Dranitsaris
@date: 2018-04-07
@organization: MLSB API
@summary: The basic admin validation API
'''
from flask.ext.restful import Resource, reqparse
from flask import request, Response
from json import dumps
from api.model import Player
from api import DB
from api.errors import PlayerDoesNotExist
from api.authentication import check_auth
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('admin_username', type=str)
post_parser.add_argument('password', type=str)

class AdminAPI(Resource):
    def post(self):
        """
            GET request for Player List
            Route: Routes['player']/<player_id: int>
            Returns:
                if found
                    status: 200 OK
                otherwise
                    status: 401 UNAUTHORIZED
        """
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(status=401)
        else:
            return Response(status=200)

    def option(self):
        return {'Allow': 'POST'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST'}