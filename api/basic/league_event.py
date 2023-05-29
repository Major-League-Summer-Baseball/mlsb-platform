'''
@author: Dallas Fraser
@date: 2023-04-29
@organization: MLSB API
@summary: The basic league event API
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api import DB
from api.model import LeagueEvent
from api.authentication import requires_admin
from api.errors import LeagueEventDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('active', type=str)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('name', type=str, required=True)
post_parser.add_argument('description', type=str, required=True)
post_parser.add_argument('active', type=str)


def convert_active(active: str) -> bool:
    """Converts active from None||1||0 to a boolean"""
    if active is None:
        return None
    return True if active == "1" else False


class LeagueEventAPI(Resource):
    def get(self, league_event_id):
        """
            GET request for a League Event Object matching given league_event_id
            Route: Routes['league_event']/<league_event_id:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {
                           'league_event_id': int,
                           'name': string,
                           'description': string
                        }
                otherwise
                    status: 404
                    mimetype: application/json
                    data:
                        None
        """
        entry = LeagueEvent.query.get(league_event_id)
        if entry is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})
        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, league_event_id):
        """
            DELETE request for league event
            Route: Routes['league_event']/<league_event_id:int>
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
        league_event = LeagueEvent.query.get(league_event_id)
        if league_event is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})

        DB.session.delete(league_event)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, league_event_id):
        """
            PUT request for league event
            Route: Routes['league_event']/<league_event_id:int>
            Parameters :
                league_event_id: The league event id (int)
                name: The name of the league event (string)
                description: The description of the league event(string)
                active: The sponsor's id (int)
            Returns:
                if found and updated successfully
                    status: 200
                    mimetype: application/json
                    data: None
                otherwise possible errors are
                    status: 404, IFSC, LEDNE
                    mimetype: application/json
                    data: None
        """
        league_event = LeagueEvent.query.get(league_event_id)
        if league_event is None:
            raise LeagueEventDoesNotExist(payload={'details': league_event_id})

        args = parser.parse_args()
        description = args.get('description', None)
        name = args.get('name', None)
        active = convert_active(args.get('active', None))

        league_event.update(name=name,
                            description=description,
                            active=active
                            )
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class LeagueEventListAPI(Resource):
    def get(self):
        """
            GET request for League Events List
            Route: Routes['league_event]
            Parameters :
            Returns:
                status: 200
                mimetype: application/json
                data:
                    league_events: [
                            {
                               'league_event_id':  int,
                               'name': string,
                               'description': string
                            }
                              ,{...}
                            ]
        """
        page = request.args.get('page', 1, type=int)
        pagination = LeagueEvent.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['league_event'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for League Event
            Route: Routes['team']
            Parameters :
                name: The name of the league event (string)
                description: The description of the league event(string)
                active: The sponsor's id (int)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created league event id (int)
                possible errors
                    status: 400, IFSC
                    mimetype: application/json
                    data: the create team id (int)
        """
        args = post_parser.parse_args()
        description = args.get('description')
        name = args.get('name')
        active = convert_active(args.get('active', "1"))

        league_event = LeagueEvent(name, description, active=active)
        DB.session.add(league_event)
        DB.session.commit()

        result = league_event.id
        return Response(dumps(result), status=201, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
