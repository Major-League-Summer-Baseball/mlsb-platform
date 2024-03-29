from flask_restful import Resource, reqparse
from flask import Response, request
from json import dumps
from api.extensions import DB
from api.model import JoinLeagueRequest as TeamRequest, Player, OAuth
from api.authentication import requires_admin
from api.errors import PlayerDoesNotExist
from api.variables import PAGE_SIZE
from api.routes import Routes
from api.helper import pagination_response
from api.cached_items import handle_table_change
from api.tables import Tables
parser = reqparse.RequestParser()
parser.add_argument('player_name', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
parser.add_argument('active', type=int)
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('player_name', type=str, required=True)
post_parser.add_argument('gender', type=str)
post_parser.add_argument('email', type=str, required=True)
post_parser.add_argument('password', type=str)
post_parser.add_argument("active", type=int)


class PlayerAPI(Resource):

    def get(self, player_id):
        """
            GET request for Player List
            Route: Routes['player']/<player_id: int>
            Returns:
                if found
                    status: 200
                    mimetype: application/json
                    data: {player_id:int, player_name:string, gender: string}
                otherwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # expose a single user
        entry = Player.query.get(player_id)
        if entry is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        response = Response(dumps(entry.json()),
                            status=200, mimetype="application/json")
        return response

    @requires_admin
    def delete(self, player_id):
        """
            DELETE request for Player
            Route: Routes['player']/<player_id: int>
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
        player = Player.query.get(player_id)
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        oauths = OAuth.query.filter(OAuth.player_id == player_id).all()
        for oauth in oauths:
            DB.session.delete(oauth)
        query = TeamRequest.query.filter(TeamRequest.email == player.email)
        for team_request in query.all():
            DB.session.delete(team_request)
        # delete a single user
        DB.session.delete(player)
        DB.session.commit()
        response = Response(dumps(None),
                            status=200, mimetype="application/json")
        handle_table_change(Tables.PLAYER, item=player.json())
        return response

    @requires_admin
    def put(self, player_id):
        """
            PUT request for Player
            Route: Routes['player']/<player_id: int>
            Parameters :
                player_name: The player's name (string)
                gender: a one letter character representing gender (string)
                email: the players email (string)
                active: 1 if player is active and 0 otherwise (int)
            Returns:
                if found and successful
                    status: 200
                    mimetype: application/json
                    data: None
                if found but new email is duplicate
                    status: NUESC
                    mimetype: application/json
                    data: None
                if found but invalid field
                    status: IFSC
                    mimetype: application/json
                    data: None
                othwerwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # update a single user
        player = DB.session.query(Player).get(player_id)
        args = parser.parse_args()
        if player is None:
            raise PlayerDoesNotExist(payload={'details': player_id})
        player_name = None
        gender = None
        email = None
        active = True
        if args['player_name']:
            player_name = args['player_name']
        if args['gender']:
            gender = args['gender']
        if args['email']:
            email = args['email']
        if args['active']:
            active = args['active'] == 1 if True else False
        player.update(name=player_name,
                      gender=gender,
                      email=email,
                      active=active)
        DB.session.commit()
        response = Response(dumps(None), status=200,
                            mimetype="application/json")
        handle_table_change(Tables.PLAYER, item=player.json())
        return response

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}


class PlayerListAPI(Resource):

    def get(self):
        """
            GET request for Player List
            Route: Routes['player']
            Returns:
                status: 200
                mimetype: application/json
                data:
                    players: [{player_id:int,
                              player-name:string,
                              gender: string,
                              active: boolean},{}
                            ]
        """
        # return a pagination of users
        page = request.args.get('page', 1, type=int)
        pagination = Player.query.paginate(page, PAGE_SIZE, False)
        result = pagination_response(pagination, Routes['player'])
        resp = Response(dumps(result), status=200,
                        mimetype="application/json")
        return resp

    @requires_admin
    def post(self):
        """
            POST request for Player List
            Route: Routes['player']
            Parameters :
                player_name: The player's name (string)
                gender: a one letter character representing gender (string)
                email: the email of the player (string)
                password: the password of the player(string)
                active: 1 if player is active and 0 otherwise (int)
            Returns:
                if successful
                    status: 200
                    mimetype: application/json
                    data: the created player id (int)
                if email is duplicate
                    status: NUESC
                    mimetype: application/json
                    data: None
                if invalid field
                    status: IFSC
                    mimetype: application/json
                    data: None
                othwerwise
                    status: 404
                    mimetype: application/json
                    data: None
        """
        # create a new user
        args = post_parser.parse_args()
        gender = "M"
        player_name = None
        email = None
        password = "default"
        active = True
        if args['player_name']:
            player_name = args['player_name']
        if args['gender']:
            gender = args['gender']
        if args['email']:
            email = args['email']
        if args['password']:
            password = args['password']
        if args['active']:
            active = args['active'] == 1 if True else False
        player = Player(player_name, email, gender, password, active=active)
        DB.session.add(player)
        DB.session.commit()
        result = player.id
        handle_table_change(Tables.PLAYER, item=player.json())
        return Response(dumps(result), status=201,
                        mimetype="application/json")

    def option(self):
        return {'Allow': 'PUT'}, 200, \
               {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT,GET'}
