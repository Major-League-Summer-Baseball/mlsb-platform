'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: The basic sponsor API
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import string_validator
from api.model import Sponsor
from api import DB
from api.authentication import requires_admin
from api.errors import SponsorDoesNotExist
parser = reqparse.RequestParser()
parser.add_argument('sponsor_name', type=str)
parser.add_argument('link', type=str)
parser.add_argument('description', type=str)
post_parser = reqparse.RequestParser()
post_parser.add_argument('sponsor_name', type=str, required=True)
post_parser.add_argument('link', type=str)
post_parser.add_argument('description', type=str)
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
                        description: string
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
        return Response(dumps(None), status=200, mimetype="application/json")

    @requires_admin
    def put(self, sponsor_id):
        """
            PUT request for Sponsor
            Route: Routes['sponsor']/<sponsor_id:int>
            Parameters :
                sponsor_name: The Sponsor's name (string)
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
        if sponsor is None:
            raise SponsorDoesNotExist(payload={'details': sponsor_id})
        args = parser.parse_args()
        if args['sponsor_name']:
            name = args['sponsor_name']
        if args['link']:
            link = args['link']
        if args['description']:
            description = args['description']
        sponsor.update(name=name, link=link, description=description)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
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
            Parameters :

            Returns:
                status: 200
                mimetype: application/json
                data:
                    Sponsors: [{sponsor_id:int,
                                sponsor_name:string,
                                description: string,
                                link: string
                                },{...}
                            ]
        """
        # return a list of Sponsors
        sponsors = Sponsor.query.all()
        for i in range(0, len(sponsors)):
            sponsors[i] = sponsors[i].json()
        resp = Response(dumps(sponsors), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Sponsor List
            Route: Routes['sponsor']/<sponsor_id:int>
            Parameters :
                sponsor_name: The Sponsor's name (string)
                link: A link to sponsors website (string)
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
        sponsor_name = None
        description = None
        link = None
        if args['sponsor_name']:
            sponsor_name = args['sponsor_name']
        if args['description']:
            description = args['description']
        if args['link']:
            link = args['link']
        print("link", link)
        sponsor = Sponsor(sponsor_name,
                          link=link,
                          description=description)
        DB.session.add(sponsor)
        DB.session.commit()
        sponsor_id = sponsor.id
        return Response(dumps(sponsor_id), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
