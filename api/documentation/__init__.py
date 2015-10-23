'''
Name: Dallas Fraser
Date: 2014-08-25
Project: MLSB API
Purpose: Holds the routes for the documentation
'''
from flask.ext.restful import Resource, reqparse
from flask import Response, render_template, make_response
from json import dumps
from api.routes import Routes

class Response(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/responseObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class Document(Resource):
    
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/documentation.html',
                                             route = Routes
                                             )
                             ,200,headers)

class PlayerObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/playerObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/teamObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class BatObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/batObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class GameObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/gameObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class LeagueObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/leagueObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class SponsorObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/sponsorObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRosterObjectDocument(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/teamRosterObject.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRosterRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/teamRosterRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/teamRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class PlayerRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/playerRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class BatRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/batRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class GameRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/gameRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class SponsorRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/sponsorRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class LeagueRoute(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/leagueRoute.html',
                                             route = Routes
                                             )
                             ,200,headers)

class TeamView(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/teamView.html',
                                             route = Routes
                                             )
                             ,200,headers)

class GameView(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/gameView.html',
                                             route = Routes
                                             )
                             ,200,headers)

class PlayerView(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation/playerView.html',
                                             route = Routes
                                             )
                             ,200,headers)
