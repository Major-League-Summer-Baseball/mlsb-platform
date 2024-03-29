from flask_restful import Resource, reqparse
from flask import Response, request
from json import dumps
from api.extensions import DB
from api.validators import string_validator
from api.model import Sponsor
from api.authentication import requires_admin
from api.errors import SponsorDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables

parser = reqparse.RequestParser()
parser.add_argument('sponsor_name', type=str)
parser.add_argument('link', type=str)
parser.add_argument('description', type=str)
parser.add_argument('active', type=int)
post_parser = reqparse.RequestParser()
post_parser.add_argument('sponsor_name', type=str, required=True)
post_parser.add_argument('link', type=str)
post_parser.add_argument('description', type=str)
post_parser.add_argument('active', type=int)
HEADERS = [{'header': 'sponsor_name', 'required': True,
            'validator': string_validator}]


class SponsorAPI(Resource):
    def get(self, sponsor_id):
        """
            GET request for Sponsor Object matching given sponsor_id
            Route: Routes['sponsor']/<sponsor_id:int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data:
                        {sponsor_id:int,
                        sponsor_name :string,
                        link: string,
                        description: string,
                        active: boolean
                        }
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # expose a single Sponsor
        entry = Sponsor.query.get(sponsor_id)
        if entry is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        response = Response(dumps(entry.json()),
                            status=200, mimetype="application/json")
        return response

    @requires_admin
    def delete(self, sponsor_id):
        """
            DELETE request for Sponsor
            Route: Routes['sponsor']/<sponsor_id:int>
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
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor is None:
            # Sponsor is not in the table
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        DB.session.delete(sponsor)
        DB.session.commit()
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return Response(dumps(None), status=200, mimetype="application/json")

    @requires_admin
    def put(self, sponsor_id):
        """
            PUT request for Sponsor
            Route: Routes['sponsor']/<sponsor_id:int>
            Parameters:
                sponsor_name: The Sponsor's name (string)
                link: the link to the sponsor (string)
                description: a description of the sponsor (string)
                active: 1 if the sponsor is active otherwise 0 (int)
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
        sponsor = Sponsor.query.get(sponsor_id)
        link = None
        description = None
        name = None
        active = True
        if sponsor is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        args = parser.parse_args()
        if args['sponsor_name']:
            name = args['sponsor_name']
        if args['link']:
            link = args['link']
        if args['description']:
            description = args['description']
        if args['active']:
            active = args['active'] == 1 if True else False
        sponsor.update(name=name,
                       link=link,
                       description=description,
                       active=active)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class SponsorListAPI(Resource):
    def get(self):
        """
            GET request for Sponsor List
            Route: Routes['sponsor']
            Parameters:
            Returns:
                status: 200
                mimetype: application/json
                data:
                    Sponsors: [{sponsor_id:int,
                                sponsor_name:string,
                                description: string,
                                link: string,
                                active: boolean
                                },{...}
                            ]
        """
        # return a pagination of Sponsors
        page = request.args.get('page', 1, type=int)
        pagination = Sponsor.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['sponsor'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Sponsor List
            Route: Routes['sponsor']/<sponsor_id:int>
            Parameters:
                sponsor_name: The Sponsor's name (string)
                link: A link to sponsors website (string)
                description: a description of the sponsor (string)
                active: 1 if the sponsor if active otherwise 0
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
        sponsor_name = None
        description = None
        link = None
        active = True
        if args['sponsor_name']:
            sponsor_name = args['sponsor_name']
        if args['description']:
            description = args['description']
        if args['link']:
            link = args['link']
        if args['active']:
            active = args['active'] == 1 if True else False
        sponsor = Sponsor(sponsor_name,
                          link=link,
                          description=description,
                          active=active)
        DB.session.add(sponsor)
        DB.session.commit()
        sponsor_id = sponsor.id
        handle_table_change(Tables.SPONSOR, item=sponsor.json())
        return Response(dumps(sponsor_id), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
