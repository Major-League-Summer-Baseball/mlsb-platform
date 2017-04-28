'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The views for fun
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import Fun
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)


class AdvancedFunAPI(Resource):
    def post(self):
        """
            POST request for Game Stats
            Route: Route['vfun']
            Parameters:
                year: the year (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: list of Fun
        """
        args = parser.parse_args()
        if args['year']:
            funs = DB.session.query(Fun).filter(Fun.year == args['year']).all()
        else:
            funs = DB.session.query(Fun).all()
        result = []
        for fun in funs:
            result.append(fun.json())
        return Response(dumps(result), status=200, mimetype="application/json")
