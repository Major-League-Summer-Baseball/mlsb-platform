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
from api.model import LeagueEventDate
from api.authentication import requires_admin
from api.errors import LeagueEventDoesNotExist, LeagueEventDateDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('date', type=str)
parser.add_argument('time', type=str)
parser.add_argument('league_event_id', type=int)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('date', type=str, required=True)
post_parser.add_argument('time', type=str, required=True)
post_parser.add_argument('league_event_id', type=int, required=True)


class LeagueEventDateAPI(Resource):
    def get(self, league_event_date_id):
        """
            GET request for a League Event date Object matching given id
            Route: Routes['league_event_date']/<league_event_date_id:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {
                           'league_event_date_id': int,
                           'league_event_date_id': int,
                           'date': string,
                           'time': string,
                           'active': boolean,
                           'description': string,
                           'name': string,
                           'attendance': int,

                        }
                otherwise
                    status: 404
                    mimetype: application/json
                    data:
                        None
        """
        entry = LeagueEventDate.query.get(league_event_date_id)
        if entry is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)

        response = Response(dumps(entry.json()), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def delete(self, league_event_date_id):
        """
            DELETE request for league event date
            Route: Routes['league_event']/<league_event_date_id:int>
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
        league_event_date = LeagueEventDate.query.get(league_event_date_id)
        if league_event_date is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)

        DB.session.delete(league_event_date)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    @requires_admin
    def put(self, league_event_date_id):
        """
            PUT request for league event
            Route: Routes['league_event']/<league_event_date_id:int>
            Parameters :
                league_event_date_id: The league event id (int)
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
        league_event_date = LeagueEventDate.query.get(league_event_date_id)
        if league_event_date is None:
            payload = {'details': league_event_date_id}
            raise LeagueEventDateDoesNotExist(payload=payload)

        args = parser.parse_args()
        league_event_id = args.get('league_event_id', None)
        date = args.get('date', None)
        time = args.get('time', None)

        league_event_date.update(league_event_id=league_event_id,
                                 date=date,
                                 time=time
                                 )
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class LeagueEventDateListAPI(Resource):
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
                               'league_event_date_id':  int,
                               'name': string,
                               'description': string
                            }
                              ,{...}
                            ]
        """
        page = request.args.get('page', 1, type=int)
        pagination = LeagueEventDate.query.paginate(page, PAGE_SIZE, False)
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

        league_event_id = args.get('league_event_id', None)
        date = args.get('date', None)
        time = args.get('time', None)

        league_event_date = LeagueEventDate(date, time, league_event_id)
        DB.session.add(league_event_date)
        DB.session.commit()
        result = league_event_date.id
        return Response(dumps(result), status=201, mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
