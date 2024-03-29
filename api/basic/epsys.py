from flask_restful import Resource, reqparse
from flask import Response, request
from json import dumps
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
        handle_table_change(Tables.ESPYS, item=espy.json())
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
                points: The points awarded (int)
                receipt: the receipt number (string)
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
        # update a single user
        espy = Espys.query.get(espy_id)
        args = parser.parse_args()
        description = None
        sponsor_id = None
        team_id = None
        points = None
        receipt = None
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
        if args['points']:
            points = args['points']
        if args['receipt']:
            receipt = args['receipt']
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        espy.update(sponsor_id=sponsor_id,
                    team_id=team_id,
                    description=description,
                    points=points,
                    receipt=receipt,
                    date=date,
                    time=time
                    )
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        handle_table_change(Tables.ESPYS, item=espy.json())
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
        # return a pagination of teams
        page = request.args.get('page', 1, type=int)
        pagination = Espys.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['espy'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Espys List
            Route: Routes['team']
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
        # create a new user
        args = post_parser.parse_args()
        description = None
        sponsor_id = None
        team_id = None
        points = None
        receipt = None
        date = None
        time = None
        if args['description']:
            description = args['description']
        if args['sponsor_id']:
            sponsor_id = args['sponsor_id']
        if args['team_id']:
            team_id = args['team_id']
        if args['points']:
            points = args['points']
        if args['receipt']:
            receipt = args['receipt']
        if args['date'] and args['time']:
            date = args['date']
            time = args['time']
        espy = Espys(sponsor_id=sponsor_id,
                     team_id=team_id,
                     description=description,
                     points=points,
                     receipt=receipt,
                     date=date,
                     time=time)
        DB.session.add(espy)
        DB.session.commit()
        result = espy.id
        handle_table_change(Tables.ESPYS, item=espy.json())
        return Response(dumps(result), status=201, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
