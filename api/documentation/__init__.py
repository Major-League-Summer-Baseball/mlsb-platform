'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: Holds the routes for the documentation
'''

'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: A view to deal with game info
'''
from flask.ext.restful import Resource, reqparse
from flask import Response, render_template, make_response
from json import dumps
from api.routes import Routes

class Response(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('responseObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class Document(Resource):
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation.html',
                                             route = Routes
                                             )
                             ,200,headers)

class PlayerObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('playerObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('teamObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class BatObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('batObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class GameObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('gameObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class LeagueObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('leagueObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class SponsorObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sponsorObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRosterObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('teamRosterObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRosterRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('teamRosterRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('teamRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class PlayerRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('playerRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class BatRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('batRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class GameRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('gameRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class SponsorRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sponsorRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class LeagueRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('leagueRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)
