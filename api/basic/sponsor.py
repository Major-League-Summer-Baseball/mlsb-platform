'''
Name: Dallas Fraser
Date: 2014-08-10
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from flask.ext.restful import Resource, reqparse
from flask import Response
from json import dumps
from api.validators import string_validator
from api.model import Sponsor
from api import DB

parser = reqparse.RequestParser()
parser.add_argument('sponsor_name', type=str)


HEADERS = [{'header':'sponsor_name', 'required':True, 
            'validator':string_validator}]


class SponsorAPI(Resource):
    def get(self, sponsor_id):
        """
            GET request for Sponsor Object matching given sponsor_id
            Route: /sponsors/<sponsor_id: int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    data:  {sponsor_id:int, sponsor_name :string, 
                            sponsoer_picture_id: int, photo_file:string}
        """
        # expose a single Sponsor
        result = {'success': False,
                  'message': '',
                  'failures':[]}
        entry  = Sponsor.query.get(sponsor_id)
        if entry is None:
            result['message'] = 'Not a valid sponsor ID'
            return Response(dumps(result), status=404,
                             mimetype="application/json")
        result['success'] = True
        result['data'] = entry.json()
        return Response(dumps(result), status=200, mimetype="application/json")


    def delete(self, sponsor_id):
        """
            DELETE request for Sponsor
            Route: /sponsors/<sponsor_id:int>
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
        """
        result = {'success': False,
                  'message': '',}
        # delete a single user
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor is None:
            #Sponsor is not in the table
            result['message'] = 'Not a valid Sponsor ID'
            return Response(dumps(result), status=400,
                            mimetype="application/json")
        DB.session.delete(sponsor)
        DB.session.commit()
        result['success'] = True
        result['message'] = 'Sponsor was deleted'
        return Response(dumps(result), status=200, mimetype="application/json")


    def put(self, sponsor_id):
        """
            PUT request for Sponsor
            Route: /sponsors/<sponsor_id:int>
            Parameters :
                sponsor_name: The Sponsor's name (string)
                sponser_picture_id: the picture for the sponser (int)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed to update 
                              (list of string)
        """
        # update a single user
        result = {'success': False,
                  'message': 'Failed to properly supply the required fields',
                  'failures':[]}
        sponsor = Sponsor.query.get(sponsor_id)
        args = parser.parse_args()
        if sponsor is None:
            result['message'] = 'Not a valid sponsor ID'
            return Response(dumps(result), status=404,
                            mimetype="application/json")
        args = parser.parse_args()
        if args['sponsor_name'] and string_validator(args['sponsor_name']):
            sponsor.name = args['sponsor_name']
            result['success'] = True
            result['message'] = ""
            DB.session.commit()
        elif args['sponsor_name'] and not string_validator(args['sponsor_name']):
            result['failures'].append("Invalid sponsor name")
        return Response(dumps(result), status=200, mimetype="application/json")


    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

class SponsorListAPI(Resource):
    def get(self):
        """
            GET request for Sponsor List
            Route: /sponsors
            Parameters :

            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    Sponsors: [{sponsor_id:int,
                              sponsor_name:string,
                              sponsor_picture_id: int
                              file: string
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

    def post(self):
        """
            POST request for Sponsor List
            Route: /sponsors
            Parameters :
                sponsor_name: The Sponsor's name (string)
            Returns:
                status: 200 
                mimetype: application/json
                data: 
                    success: tells if request was successful (boolean)
                    message: the status message (string)
                    failures: a list of parameters that failed (list of string)
                    sponsor_id: the created user Sponsor id (int)
        """
        # create a new user
        result = {'success': False,
                  'message': '',
                  'failures': [],
                  'sponsor_id': None}
        args = parser.parse_args()
        sponsor_name = None
        if args['sponsor_name'] and string_validator(args['sponsor_name']):
            sponsor_name = args['sponsor_name']
        else:
            result['failures'].append("Invalid sponsor name")
        if len(result['failures']) > 0:
            result['message'] = "Failed to properly supply the required fields"
            return Response(dumps(result), status=400,
                        mimetype="application/json")
        sponsor = Sponsor(sponsor_name)
        DB.session.add(sponsor)
        DB.session.commit()
        result['sponsor_id'] = sponsor.id
        result['data'] = sponsor.json()
        result['success'] = True
        return Response(dumps(result), status=200,
                        mimetype="application/json")
 
    def options (self):
        return {'Allow' : 'PUT' }, 200, \
                { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }
