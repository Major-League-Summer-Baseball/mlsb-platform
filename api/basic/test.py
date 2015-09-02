'''
@author: Dallas Fraser
@author: 2015-08-25
@organization: MLSB API
@summary: Tests all the basic APIs
'''
from api import app
import unittest
import os
import tempfile
from api.helper import loads
from api import DB
from pprint import PrettyPrinter
from api.routes import Routes
from api.model import Player, Team, Sponsor, League, Game, Bat, roster
from datetime import datetime
class BaseTest(unittest.TestCase):

    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')
        print("Starting Test")
        DB.create_all()

    def tearDown(self):
        DB.engine.execute('''   
                                DROP TABLE IF EXISTS roster;
                                DROP TABLE IF EXISTS bat;
                                DROP TABLE IF EXISTS game;
                                DROP TABLE IF EXISTS team;
                                DROP TABLE IF EXISTS player;
                                DROP TABLE IF EXISTS sponsor;
                                DROP TABLE IF EXISTS league;
                        ''')

    def output(self, data):
        if self.show_results:
            self.pp.pprint(data)

    def addSponsor(self):
        self.sponsor = Sponsor("Domus")
        DB.session.add(self.sponsor)
        DB.session.commit()
        self.assertEqual(self.sponsor.id, 1, "Could not add sponsor")

    def addSpsonors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
            DB.session.commit()
            self.assertEqual(s, self.sponsors[s].id)

    def addPlayer(self):
        p = Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m")
        DB.session.add(p)
        DB.session.commit()
        self.assertEqual(p.id, 1, "Could not add player")

    def addPlayers(self):
        players = [Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m"),
                   Player("My Dream Girl",
                   "dream@mylaurier.ca",
                   gender="f"),
                   Player("Barry Bonds",
                          "bonds@hallOfFame.ca",
                          gender="M")]
        for player in range(0, len(players)):
            DB.session.add(players[player])
            DB.session.commit()
            self.assertEqual(player, players[player].id)

    def addTeam(self):
        self.addPlayer()
        self.addSponsor()
        self.team = Team(color="Green")
        self.team.sponsor_id = self.sponsor.id
        DB.session.add(self.team)
        DB.session.commit()
        self.assertEqual(self.team.id, 1)

    def addTeams(self):
        self.addPlayers()
        self.addSponsors()
        # team one
        self.teams = [Team(color="Green"),
                      Team(color="Black")
                      ]
        self.teams[0].sponsor_id = self.sponsors[0].id
        self.teams[1].sponsor_id = self.sponsors[1].id
        for t in range(0, len(self.teams)):
            DB.session.add(self.teams[t])
            DB.sesssion.commit()
            self.assertEqual(t, self.teams[t].id)

    def addLeague(self):
        self.league = League("Monday & Wedneday")
        DB.session.add(self.league)
        DB.session.commit()
        self.assertEqual(0, self.league.id)

    def addGame(self):
        self.addTeams()
        self.addLeague()
        self.game = Game(datetime.now(),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.league.id)
        DB.session.add(self.game)
        DB.session.commit()
        self.assertEqual(0, self.game.id)

    def addBat(self):
        self.addGame()
        self.bat = Bat(self.players[0].id,
                       self.teams[0].id,
                       self.game.id,
                       "S",
                       5,
                       rbi=1)
        DB.session.add(self.bat)
        DB.session.commit()
        self.assertEqual(self.bat.id, 1)

    def addPlayerToTeam(self):
        self.addLeague()
        self.addTeam()
        params = {'team_id': 1, "player_id": 1, 
                  "start_date": "2014-08-28", 'tournament_id': 1}
        rv = self.app.post(Routes['team_roster'], data=params)
        expect = {'failures': [], 'message': 'Successful roster addition',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: valid data")

class TestSponsor(BaseTest):
    def testSponsorListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['sponsor'])
        empty = loads(rv.data)
        self.assertEqual([], empty,"/sponsors GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['sponsor'], data=params)
        result ={"sponsor_id": None,
                 "failures": ['Invalid sponsor name'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['sponsor']
                         + " POST: POST request with missing parameter"
                         )
        # testing with improper name parameters
        params = {'sponsor_name':1, 'sponsor_picture_id':1}
        rv = self.app.post(Routes['sponsor'], data=params)
        result = {"sponsor_id": None, 
                  "failures": ['Invalid sponsor name'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['sponsor']
                         + " POST: POST request with invalid parameters"
                         )
        # proper insertion with post
        params = {'sponsor_name':"Domus"}
        rv = self.app.post(Routes['sponsor'], data=params)
        result = {  'data': {
                              'sponsor_id': 1,
                              'sponsor_name': 'Domus'},
                    'failures': [],
                    'message': '',
                    'sponsor_id': 1,
                    'success': True}
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
       
        #test a get with sponsors
        rv = self.app.get(Routes['sponsor'])
        result = [   {  'sponsor_id': 1,
                        'sponsor_name': 'Domus'}
                 ]
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(result, loads(rv.data), Routes['sponsor']
                         + " GET Failed to return list of tournaments")

    def testSponsorAPIGet(self):
        # proper insertion with post
        self.addSponsor()
        # invalid sponsor
        rv = self.app.get(Routes['sponsor']+ "/2")
        expect = {'failures': [],
                  "message": "Not a valid sponsor ID",
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " Get: Invalid Sponsor")
        # valid sponsor
        rv = self.app.get(Routes['sponsor']+ "/1")
        data = { 'sponsor_id': 1,
                 'sponsor_name': 'Domus',}
        expect = {'data': data,
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " Get: Valid Sponsor")

    def testSponsorAPIDelete(self):
        #proper insertion with post
        self.addSponsor()
        # delete of invalid sponsor id
        rv = self.app.delete(Routes['sponsor'] + "/2")
        result = {'message': 'Not a valid Sponsor ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result,
                         Routes['sponsor'] + " DELETE Invalid Sponsor id ")
        # delete valid sponsor id
        rv = self.app.delete(Routes['sponsor'] + "/1")
        result = {  'message': 'Sponsor was deleted', 
                    'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result,
                         Routes['photo'] + ' DELETE Valid sponsor id')

    def testSponsorAPIPut(self):
        #proper insertion with post
        self.show_results = True
        self.addSponsor()
        #invalid sponsor id
        params = {'sponsor_name': 'New League'}
        rv = self.app.put(Routes['sponsor'] + '/2', data=params)
        expect = {'failures': [], 'message': 'Not a valid sponsor ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        #invalid parameters
        params = {'sponsor_name': 1}
        rv = self.app.put(Routes['sponsor'] + '/1', data=params)
        expect = {'failures': ['Invalid sponsor name'],
                  'message': 'Failed to properly supply the required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid parameters")
        #successful update
        params = {'sponsor_name': 'New League'}
        rv = self.app.put(Routes['sponsor'] + '/1', data=params)
        expect = {  'failures': [],
                    'message': '',
                    'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")

class TestPlayer(BaseTest):
    def testPlayerApiGet(self):
        # proper insertion with post
        self.addPlayer()
        # invalid player id
        rv = self.app.get(Routes['player'] + "/2")
        result = {'failures': [], 'message': 'Not a valid player ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['player'] +
                         " GET invalid player id")
        # valid user
        rv = self.app.get(Routes['player'] + "/1")
        data = {"player_id": 1,
                'email': 'fras2560@mylaurier.ca',
                'gender': 'm',
                'player_name': 'Dallas Fraser'}
        result = {'data': data,
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['player'] +
                         " GET valid player id")

    def testPlayerApiDelete(self):
        # proper insertion with post
        self.addPlayer()
        # delete of invalid player id
        rv = self.app.delete(Routes['player'] + "/2")
        result = {'message': 'Not a valid player ID', 'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['player'] +
                         " DELETE Invalid player id ")
        rv = self.app.delete(Routes['player'] + "/1")
        result = {'message': 'Player was deleted', 'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['player'] +
                         ' DELETE Valid player id')

    def testPlayerApiPut(self):
        # must add a player
        self.addPlayer()
        # invalid player id
        params = {'player_name':'David Duchovny', 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/2', data=params)
        result = {"failures": [],
                  "message": "Not a valid player ID",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player ID')
        # invalid player_name type
        params = {'player_name':1, 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/1', data=params)
        result = {"failures": ["Invalid player name"],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['player'] +
                         ' PUT: Invalid Player name')
        # invalid gender
        params = {'player_name':"David Duchovny", 'gender':"X"}
        rv = self.app.put(Routes['player'] + '/1', data=params)
        result = {"failures": ["Invalid gender"],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['player'] +
                         ' PUT: Invalid Player gender')
        # successfully update
        params = {'player_name':"David Duchovny", 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/1', data=params)
        result = {"failures": [],
                  "message": "",
                  "success": True
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['player'] +
                         ' PUT: Valid player update')

    def testPlayerListApi(self):
        # test an empty get
        rv = self.app.get(Routes['player'])
        empty = loads(rv.data)
        self.assertEqual([], empty,Routes['player'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['player'], data=params)
        result ={"player_id": None,
                 "failures": ['Invalid player name'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['player'] +
                         " POST: POST request with missing parameter"
                         )
        # testing a gender parameter
        params = {'player_name':'Dallas Fraser','gender':'X'}
        rv = self.app.post(Routes['player'], data=params)
        result = {"player_id": None,
                  "failures": ['Invalid gender'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        params = {'player_name':'Dallas Fraser','gender':1}
        rv = self.app.post(Routes['player'], data=params)
        result = {"player_id": None,
                  "failures": ['Invalid gender'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        # testing player_name parameter
        params = {'player_name':1,'gender':'M'}
        rv = self.app.post(Routes['player'], data=params)
        result = {"player_id": None,
                  "failures": ['Invalid player name'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid name"
                         )
        #proper insertion with post
        params = {'player_name':"Dallas Fraser",
                      "gender": "M",
                      "email": "fras2560@mylaurier.ca",
                      "password":"Suck it"}
        rv = self.app.post(Routes['player'], data=params)
        result = {  'data': {
                              'email': 'fras2560@mylaurier.ca',
                              'gender': 'm',
                              'player_id': 1,
                              'player_name': 'Dallas Fraser'},
                    'failures': [],
                    'message': '',
                    'player_id': 1,
                    'success': True}
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        rv = self.app.get(Routes['player'])
        empty = loads(rv.data)
        expect = [{'email': 'fras2560@mylaurier.ca',
                   'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'}]
        self.assertEqual(expect, empty,Routes['player'] +
                         " GET: did not receive player list")
        

class TestTournament(BaseTest):
    def testTournamentAPIGet(self):
        # proper insertion with post
        self.addLeague()
        # invalid tournament id
        rv = self.app.get(Routes['tournament'] + "/2")
        result = {'failures': [],
                  'message': 'Not a valid tournament ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['tournament'] +
                         " GET invalid tournament id")
        # valid tournament id
        rv = self.app.get(Routes['tournament'] + "/1")
        result = {'data': {"tournament_id": 1, "tournament_name": "League"},
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['tournament'] +
                         " GET valid tournament id")


    def testTournamentAPIDelete(self):
        # proper insertion with post
        self.addLeague()
        # delete of invalid tournament id
        rv = self.app.delete(Routes['tournament'] + "/2")
        result = {'message': 'Not a valid Tournament ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['tournament']+
                         " DELETE Invalid tournament id ")
        rv = self.app.delete(Routes['tournament'] + "/1")
        result = {  'message': 'Tournament was deleted', 
                    'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['tournament'] +
                         ' DELETE Valid tournament id')


    def testTournamentAPIPut(self):
        # must add a tournament
        self.addLeague()
        # invalid tournament id
        params = {'tournament_name':'Chainsaw Classic'}
        rv = self.app.put(Routes['tournament'] + '/2', data=params)
        result = {"failures": [],
                  "message": "Not a valid tournament ID",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['tournament'] + 
                         ' PUT: Invalid tournament ID')
        # invalid tournament_name type
        params = {'tournament_name':1}
        rv = self.app.put(Routes['tournament'] + '/1', data=params)
        result = {"failures": ["Invalid data for header tournament_name"],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result)
        # successfully update
        params = {'tournament_name':"Chainsaw Classic"}
        rv = self.app.put(Routes['tournament'] + '/1', data=params)
        result = {"failures": [],
                  "message": "Successfully updated the tournament",
                  "success": True
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result)


    def testTournamentListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['tournament'])
        empty = loads(rv.data)
        self.assertEqual([], empty,Routes['tournament'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['tournament'], data=params)
        result ={"tournament_id": None,
                 "failures": ['Missing header tournament_name'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['tournament'] +
                         " POST: request with missing parameter"
                         )
        # testing a gender parameter
        params = {'tournament_name':1}
        rv = self.app.post(Routes['tournament'], data=params)
        result = {"tournament_id": None,
                  "failures": ['Invalid data for header tournament_name'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['tournament'] + 
                         " POST: request with invalid tournament_name"
                         )
        # proper insertion with post
        self.addLeague()
        # test a get with tournaments
        rv = self.app.get(Routes['tournament'])
        result = [{'tournament_id': 1,'tournament_name':"League"}]
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(result, loads(rv.data), Routes['tournament'] + 
                         " GET: Failed to return list of tournaments")

class TestTeam(BaseTest):
    def testTeamListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['team'])
        empty = loads(rv.data)
        self.assertEqual([], empty,
                         Routes['team'] + " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['team'], data=params)
        result ={"team_id": None,
                 "failures": ['Missing header team_name'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['team']
                         + " POST: request with missing parameter"
                         )
        # testing a all invalid parameters
        params = {'team_name': 1,
                  'captain_id': 1,
                  'sponsor_id': 1,
                  'team_photo_id': 1,
                  'color': 1}
        rv = self.app.post(Routes['team'], data=params)
        result = {"team_id": None,
                  "failures": ['Invalid data for header team_name',
                               'Invalid data for header captain_id',
                               'Invalid data for header sponsor_id',
                               'Invalid data for header color',
                               'Invalid data for header team_photo_id'], 
                  "message": "Failed to properly supply the required fields", 
                  "success": False
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # proper insertion with post
        self.addTeam()
        # test a get with team
        rv = self.app.get(Routes['team'])
        expect = [{ 'captain_id': 1,
                    'color': 'Green',
                    'sponsor_id': 1,
                    'team_id': 1,
                    'team_name': 'Domus Green',
                    'team_photo_id': 1}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team']
                         + " GET: Failed to return list of teams")

    def testTeamGet(self):
        # proper insertion with post
        self.addTeam()
        # test invalid team id
        rv = self.app.get(Routes['team'] + "/2")
        expect = {'failures': [], 'message': 'Not a valid team ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " GET: invalid team id")
        # test valid team id
        rv = self.app.get(Routes['team'] + "/1")
        data = {'captain_id': 1,
                'color': 'Green',
                'sponsor_id': 1,
                'team_id': 1,
                'team_name': 'Domus Green',
                'team_photo_id': 1}
        expect = {'data': data,
                'failures': [],
                'message': '',
                'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] + 
                         " GET: valid team id")

    def testTeamDelete(self):
        # proper insertion with post
        self.addTeam()
        # delete of invalid team id
        rv = self.app.delete(Routes['team'] + "/2")
        result = {'message': 'Not a valid Team ID', 'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['team'] +
                         " DELETE: Invalid team id ")
        rv = self.app.delete(Routes['team'] + "/1")
        result = {'message': 'Team was deleted', 'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['team'] +
                         ' DELETE: Valid team id')

    def testTeamPut(self):
        # proper insertion with post
        self.addTeam()
        # invalid team id
        params = {'team_name': "Chainsaw Black",
                  'captain_id': 1,
                  'sponsor_id': 1,
                  'team_photo_id': 1,
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/2', data=params)
        expect = {'failures': [], 'message': 'Not a valid Team ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid team ID")
        # invalid parameters
        params = {'team_name': 1,
                  'captain_id': 2,
                  'sponsor_id': 2,
                  'team_photo_id': 2,
                  'color': 1}
        rv = self.app.put(Routes['team'] + '/1', data=params)
        expect = {  'failures': ['Invalid data for header team_name',
                               'Invalid data for header captain_id',
                               'Invalid data for header sponsor_id',
                               'Invalid data for header color',
                               'Invalid data for header team_photo_id'],
                    'message': 'Failed to properly supply the required fields',
                    'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid parameters")
        # successful update
        # insert second picture
        fp = os.path.join("pictures", "test2.jpg")
        params = {'file_path':fp}
        rv = self.app.post(Routes['photo'], data=params)
        expect = {"photo_id": 2, "failures": [],
                  "message": "Successfully created photo", "success": True
                 }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, 
                         Routes['photo'] + " POST: Failed to create a photo"
                         )
        # insert second sponsor
        params = {'sponsor_name': 'New League', 'sponsor_picture_id': 2}
        rv = self.app.post(Routes['sponsor'], data=params)
        expect = {"sponsor_id": 2, "failures": [], 
                                "message": "Successfully created Sponsor", 
                                "success": True
                             }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")
        # insert second captain
        params = {'player_name':'Barry Bonds','gender':'M'}
        rv = self.app.post('/players', data=params)
        expect = {"player_id": 2, "failures": [], 
                  "message": "Successfully created player", "success": True
                 }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, 
                         Routes['player'] + " POST: Failed to create a player"
                         )
        # valid update
        params = {'team_name': "Chainsaw Black",
                  'captain_id': 2,
                  'sponsor_id': 2,
                  'team_photo_id': 2,
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/1', data=params)
        expect = {'failures': [], 'message': 'Successfully updated the Team',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " PUT: Failed to update a team")

class TestGame(BaseTest):
    def testGameListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['game'])
        empty = loads(rv.data)
        self.assertEqual([], empty,
                        Routes['game'] + "GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['game'], data=params)
        expect = {'failures': ['Missing header date',
                               'Missing header tournament_id',
                               'Missing header time'],
                  'game_id': None,
                  'message': 'Failed to properly supply the required fields',
                  'success': False
                  }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")
        # testing all invalid parameters
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-2014", 
                  'time': "25:61",
                  'tournament_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params)
        expect = {'failures': [ 'Invalid data for header home_team_id',
                                'Invalid data for header away_team_id',
                                'Invalid data for header date',
                                'Invalid data for header tournament_id',
                                'Invalid data for header time'],
                  'game_id': None,
                  'message': 'Failed to properly supply the required fields',
                  'success': False
                 }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")
        # test valid parameters
        self.addGame()

    def testGameGet(self):
        # proper insertion
        self.addGame()
        # invalid id
        rv = self.app.get(Routes['game'] + "/2")
        expect = {'failures': [], 'message': 'Not a valid game ID',
                  'success': False}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " GET: with invalid game id")
        # valid id
        rv = self.app.get(Routes['game'] + "/1")
        data = {'away_team_id': 2,
                'date': '2014-08-23',
                'game_id': 1,
                'home_team_id': 1,
                'time': '11:38',
                'tournament_id': 1}
        expect = {'data': data,
                  'failures': [],
                  'message': '',
                  'success': True
                }
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " GET: with valid game id")

    def testGameDelete(self):
        # proper insertion
        self.addGame()
        # delete invalid game id
        rv = self.app.delete(Routes['game'] + "/2")
        expect = {'message': 'Not a valid Game ID', 'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] + 
                         " DELETE: on invalid game id")
        # delete valid game id
        rv = self.app.delete(Routes['game'] + "/1")
        expect = {'message': 'Game was deleted', 'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] + 
                         " DELETE: on valid game id")

    def testGamePut(self):
        # proper insertion
        self.addGame()
        # add second tournament
        params = {'tournament_name':'Chainswa Classic'}
        rv = self.app.post(Routes['tournament'], data=params)
        result = {"tournament_id": 2, "failures": [],
                  "message": "Successfully created tournament",
                  "success": True
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['tournament']
                         + " POST: Failed to create a tournament"
                         )
        # invalid game id
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'tournament_id': 2
                 }
        rv = self.app.put(Routes['game'] + "/2", data=params)
        expect = {'failures': [], 'message': 'Not a valid Game ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid game id")
        # testing invalid parameters
        params = {
                  'home_team_id': 3,
                  'away_team_id': 4,
                  'date': "2014-08-35",
                  'time': "11:62",
                  'tournament_id': 3
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params)
        expect = {'failures': ['Invalid data for header home_team_id',
                               'Invalid data for header away_team_id',
                               'Invalid data for header date',
                               'Invalid data for header tournament_id',
                               'Invalid data for header time'],
                  'message': 'Failed to properly supply the required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid parameters")
        # valid update parameters
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'tournament_id': 2
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params)
        expect = {'failures': [], 'message': 'Successfully updated the Game',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: valid update")

class TestBat(BaseTest):
    def testBatList(self):
        # test an empty get
        rv = self.app.get(Routes['bat'])
        empty = loads(rv.data)
        self.assertEqual([], empty,
                        Routes['bat'] + "GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['bat'], data=params)
        expect = {'bat_id': None,
                  'failures': ['Missing header player_id',
                               'Missing header rbi',
                               'Missing header classification',
                               'Missing header game_id',
                               'Missing header team_id'],
                  'message': 'Failed to properly supply the required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with missing parameters")
        # testing all invalid parameters
        params = {
                  'game_id': 1,
                  'player_id': 3,
                  'rbi': 10, 
                  'classification': "X",
                  'team': 'away'
                              }
        rv = self.app.post(Routes['bat'], data=params)
        expect = {'bat_id': None,
                  'failures': ['Invalid data for header player_id',
                               'Invalid data for header rbi',
                               'Invalid data for header classification',
                               'Invalid data for header game_id',
                               'Missing header team_id'],
                  'message': 'Failed to properly supply the required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with missing parameters")
        # test all valid parameters
        self.addBat()

    def testBatGet(self):
        # proper insertion of get
        self.addBat()
        # get on invalid id
        rv = self.app.get(Routes['bat']+ "/2")
        expect = {'failures': [], 'message': 'Not a valid bat ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " GET: invalid bat id")
        # get on valid id
        rv = self.app.get(Routes['bat']+ "/1")
        data = {'bat_id': 1,
                'classification': 'HR',
                'game_id': 1,
                'player_id': 1,
                'rbi': 4,
                'team_id': 1}
        expect = {'data': data,
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " GET: valid bat id")

    def testBatDelete(self):
        # proper insertion of get
        self.addBat()
        # delete invalid id
        rv = self.app.delete(Routes['bat']+ "/2")
        expect = {'message': 'Not a valid Bat ID', 'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " DELETE: invalid bat id")
        # delete valid id
        rv = self.app.delete(Routes['bat']+ "/1")
        expect = {'message': 'Bat was deleted', 'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " DELETE: valid bat id")

    def testBatPut(self):
        # proper insertion of get
        self.addBat()
        # add a second game
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-24", 
                  'time': "11:30",
                  'tournament_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params)
        expect = { 'failures': [],
                   'game_id': 2,
                   'message': 'Successfully created game',
                   'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: with valid parameterss")
        # invalid bat id
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'rbi': 4, 
                  'classification': "HR",
                              }
        rv = self.app.put(Routes['bat'] + "/2", data=params)
        expect = {'failures': [], 'message': 'Not a valid Bat ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid Bat id")
        # test invalid parameters
        params = {
                  'game_id': 3,
                  'player_id': 4,
                  'rbi': 5, 
                  'classification': "X",
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params)
        expect = {'failures': ['Invalid data for header player_id',
                               'Invalid data for header rbi',
                               'Invalid data for header classification',
                               'Invalid data for header game_id'],
                  'message': 'Failed to properly supply the required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid parameters")
        # valid update
        params = {
                  'game_id': 2,
                  'player_id': 2,
                  'rbi': 3, 
                  'classification': "S",
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params)
        expect = {'failures': [], 'message': 'Successfully updated the Bat',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: valid parameters")

class TestTeamRoster(BaseTest):
    def testPost(self):
        #invalid update
        params = {'team_id': 1, "player_id": 1, 
                  "start_date": "2014/08/8", 'tournament_id': 1}
        rv = self.app.post(Routes['team_roster'], data=params)
        expect = {'failures': ['Invalid data for header player_id',
                               'Invalid data for header team_id',
                               'Invalid data for header tournament_id',
                               'Invalid data for header start_date'],
                  'message': 'Failed to properly supply the certain fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: invalid data")
        # add player to team        
        self.addPlayerToTeam()

    def testDelete(self):
        #add player to team
        self.addPlayerToTeam()
        # missing data
        query = "?team_id=2"
        rv = self.app.delete(Routes['team_roster'] + query)
        expect = {'failures': ['Missing header Player and Team id'],
                  'message': 'Failed to supply required fields',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Missing header")
        # invalid combination
        query = "?team_id=2&player_id=2"
        rv = self.app.delete(Routes['team_roster'] + query)
        expect = {'failures': [], 'message': 'Invalid combination',
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")
        # proper deletion
        query = "?team_id=1&player_id=1"
        rv = self.app.delete(Routes['team_roster'] + query)
        expect = {'failures': [], 'message': 'Removed player from team', 
                  'success': True}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")

    def testGet(self):
        #empty get
        rv = self.app.get(Routes['team_roster'])
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on empty set")
        self.addPlayerToTeam()
        rv = self.app.get(Routes['team_roster'])
        expect = [
                   {'end_date': None,
                   'player_id': 1,
                   'start_date': '2014-08-28',
                   'team_id': 1,
                   'tournament_id': 1
                   }
                 ]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on non-empty set")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()