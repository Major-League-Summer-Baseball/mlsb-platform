'''
@author: Dallas Fraser
@date: 2015-08-25
@organization: MLSB API
@summary: The basic espys API
'''

from flask.ext.restful import Resource, reqparse, inputs
from flask import Response
from json import dumps
from api import DB
from api.model import Espys
from api.authentication import requires_admin, requires_player
from api.errors import EspysDoesNotExist
parser = reqparse.RequestParser()
parser.add_argument('sponsor_id', type=int)
parser.add_argument('team_id', type=int)
parser.add_argument('player_id', type=int)
parser.add_argument('description', type=str)
parser.add_argument('points', type=str)
parser.add_argument('receipt', type=str)
parser.add_argument('receipt_image', type=str)
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('approved', type=inputs.boolean)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('sponsor_id', type=int)
post_parser.add_argument('team_id', type=int, required=True)
post_parser.add_argument('player_id', type=int)
post_parser.add_argument('description', type=str)
post_parser.add_argument('points', type=str, required=True)
post_parser.add_argument('receipt', type=str)
post_parser.add_argument('receipt_image', type=str)
post_parser.add_argument('date', type=str)
post_parser.add_argument('time', type=str)
post_parser.add_argument('approved', type=inputs.boolean)


class EspyAPI(Resource):
    def get(self, espy_id):
        """
            GET request for Espys Object matching given espy_id
            Route: Routes['team']/<espy_id:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {
                           'date':  date,
                           'team': string,
                           'sponsor': string,
                           'description': string,
                           'points': int,
                           'receipt': string
                        }
                otherwise
                    status: 404
                    mimetype: application/json
                    data:
                        None
        """
        # expose a single team
        entry = Espys.query.get(espy_id)
        if entry is None:
            raise EspysDoesNotExist(payload={'details': espy_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, espy_id):
        """
            DELETE request for Espy
            Route: Routes['espy']/<espy_id:int>
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
        espy = Espys.query.get(espy_id)
        if espy is None:
            raise EspysDoesNotExist(payload={'details': espy_id})
        # delete a single espy
        DB.session.delete(espy)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, espy_id):
        """
            PUT request for espy
            Route: Routes['team']/<espy_id:int>
            Parameters :
                espy_id: The espy's id (int)
                description: The description of the transaction (string)
                sponsor_id: The sponsor's id (int)
                team_id: The team's id (int)
                player_id: The player's id (int)
                points: The points awarded (int)
                receipt: the receipt number (string)
                approved: boolean
            Returns:
                if found and updated successfully
                    status: 200
                    mimetype: application/json
                    data: None
                otherwise possible errors are
                    status: 404, IFSC, TDNESC, SDNESC
                    mimetype: application/json
                    data: None
        """
        # update a single espy
        espy = Espys.query.get(espy_id)
        args = parser.parse_args()
        description = None
        sponsor_id = None
        team_id = None
        player_id = None
        points = None
        receipt = None
        receipt_image = None
        approved = False
        date = None
        time = None
        if espy is None:
            raise EspysDoesNotExist(payload={'details': espy_id})
        if args['description']:
            description = args['description']
        if args['sponsor_id']:
            sponsor_id = args['sponsor_id']
        if args['team_id']:
            team_id = args['team_id']
        if args['player_id']:
            team_id = args['player_id']
        if args['points']:
            points = args['points']
        if args['receipt']:
            receipt = args['receipt']
        if args['receipt_image']:
            receipt = args['receipt_image']
        if args['approved']:
            approved = args['approved']
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        espy.update(sponsor_id=sponsor_id,
                    team_id=team_id,
                    description=description,
                    points=points,
                    receipt=receipt,
                    date=date,
                    time=time,
                    player_id=player_id,
                    receipt_image=receipt_image
                    )
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class EspyListAPI(Resource):
    def get(self):
        """
            GET request for Espys List
            Route: Routes['espy']
            Parameters :
            Returns:
                status: 200
                mimetype: application/json
                data:
                    teams: {
                            {
                               'date':  date,
                               'team': string,
                               'sponsor': string,
                               'description': string,
                               'points': int,
                               'receipt': string
                            }
                              ,{...}
                            ]
        """
        # return a list of espys
        espys = Espys.query.all()
        result = []
        for i in range(0, len(espys)):
            result.append(espys[i].json())
        resp = Response(dumps(result), status=200, mimetype="application/json")
        return resp

    @requires_player
    def post(self):
        """
            POST request for Espys List
            Route: Routes['espy']
            Parameters :
                league_id: the league's id (int)
                sponsor_id: the sponsor's id (int)
                color: the color of the team (string)
                year: the year the team is playing in (int)
                espys: the team espys points (int)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the create team id (int)
                possible errors
                    status: 400, IFSC, LDNESC, PDNESC or SDNESC
                    mimetype: application/json
                    data: the create team id (int)
        """
        # create a new espy
        args = post_parser.parse_args()
        description = None
        sponsor_id = None
        team_id = None
        player_id = None
        points = None
        receipt = None
        receipt_image = None
        date = None
        time = None
        if args['description']:
            description = args['description']
        if args['sponsor_id']:
            sponsor_id = args['sponsor_id']
        if args['team_id']:
            team_id = args['team_id']
        if args['player_id']:
            player_id = args['player_id']
        if args['points']:
            points = args['points']
        if args['receipt']:
            points = args['receipt']
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        espy = Espys(sponsor_id=sponsor_id,
                     team_id=team_id,
                     player_id=player_id,
                     description=description,
                     points=points,
                     receipt=receipt,
                     receipt_image=receipt_image,
                     date=date,
                     time=time)
        DB.session.add(espy)
        DB.session.commit()
        result = espy.id
        return Response(dumps(result), status=201, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}

class EspyListPendingAPI(Resource):
    @requires_admin
    def get(self):
        """
            GET request for Espys List which are not yet approved (for admins)
            Route: Routes[]
            Parameters :
            Returns:
                status: 200
                mimetype: application/json
                data:
                    espy: {
                            {
                               'espy_id': int,
                               'date':  date,
                               'team': string,
                               'sponsor': string,
                               'description': string,
                               'points': int,
                               'receipt': string
                               'player': string,
                               'receipt_image', binary string
                            }
                              ,{...}
                            ]
        """
        # return a list of espys
        espys = Espys.query.filter(Espys.approved == False).all()
        result = []
        for i in range(0, len(espys)):
            result.append(espys[i].json())
        response = Response(dumps(result), status=200, mimetype="application/json")
        return response

        def option(self):
            return {'Allow': 'GET'}, 200, \
                    {'Access-Control-Allow-Origin': '*',
                     'Access-Control-Allow-Methods': 'GET'}