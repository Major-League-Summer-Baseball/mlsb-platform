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
from datetime import datetime, date, time

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = date(2014, 8, 23)
        self.t = time(11, 37)
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

    def addSponsors(self):
        self.sponsors = [Sponsor("Domus"),
                         Sponsor("Chainsaw")
                         ]
        for s in range(0,len(self.sponsors)):
            DB.session.add(self.sponsors[s])
        DB.session.commit()

    def addPlayer(self):
        p = Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m")
        DB.session.add(p)
        DB.session.commit()
        self.assertEqual(p.id, 1, "Could not add player")

    def addPlayers(self):
        self.players = [Player("Dallas Fraser",
                   "fras2560@mylaurier.ca",
                   gender="m"),
                   Player("My Dream Girl",
                   "dream@mylaurier.ca",
                   gender="f"),
                   Player("Barry Bonds",
                          "bonds@hallOfFame.ca",
                          gender="M")]
        for player in range(0, len(self.players)):
            DB.session.add(self.players[player])
        DB.session.commit()

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
        DB.session.commit()

    def addLeague(self):
        self.league = League("Monday & Wedneday")
        DB.session.add(self.league)
        DB.session.commit()
        self.assertEqual(1, self.league.id)

    def addLeagues(self):
        self.leagues = [League("Monday & Wedneday"), League("Tuesday & Thursday")]
        for t in range(0, len(self.leagues)):
            DB.session.add(self.leagues[t])
        DB.session.commit()

    def addGame(self):
        self.addTeams()
        self.addLeague()
        self.game = Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.league.id)
        DB.session.add(self.game)
        DB.session.commit()
        self.assertEqual(1, self.game.id)

    def addGames(self):
        self.addTeams()
        self.addLeagues()
        self.games = [Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[0].id),
                      Game(datetime.combine(self.d, self.t),
                         self.teams[0].id,
                         self.teams[1].id,
                         self.leagues[1].id)
                      ]
        DB.session.add(self.games[0])
        DB.session.add(self.games[1])
        DB.session.commit()

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
        
class TestLeague(BaseTest):
    def testLeagueAPIGet(self):
        # proper insertion with post
        self.addLeague()
        # invalid league id
        rv = self.app.get(Routes['league'] + "/2")
        result = {'failures': [],
                  'message': 'Not a valid league ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['league'] +
                         " GET invalid league id")
        # valid league id
        rv = self.app.get(Routes['league'] + "/1")
        result = {'data': {"league_id": 1, "league_name": "Monday & Wedneday"},
                  'failures': [],
                  'message': '',
                  'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['league'] +
                         " GET valid league id")

    def testLeagueAPIDelete(self):
        # proper insertion with post
        self.addLeague()
        # delete of invalid league id
        rv = self.app.delete(Routes['league'] + "/2")
        result = {'message': 'Not a valid league ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['league']+
                         " DELETE Invalid league id ")
        rv = self.app.delete(Routes['league'] + "/1")
        result = {  'message': 'League was deleted', 
                    'success': True}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['league'] +
                         ' DELETE Valid league id')

    def testLeagueAPIPut(self):
        # must add a League
        self.addLeague()
        # invalid league id
        params = {'league_name':'Chainsaw Classic'}
        rv = self.app.put(Routes['league'] + '/2', data=params)
        result = {"failures": [],
                  "message": "Not a valid league ID",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result, Routes['league'] + 
                         ' PUT: Invalid league ID')
        # invalid league_name type
        params = {'league_name':1}
        rv = self.app.put(Routes['league'] + '/1', data=params)
        result = {"failures": ["Invalid league name"],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result)
        # successfully update
        params = {'league_name':"Chainsaw Classic"}
        rv = self.app.put(Routes['league'] + '/1', data=params)
        result = {"failures": [],
                  "message": "",
                  "success": True
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result)

    def testTournamentListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['league'])
        empty = loads(rv.data)
        self.assertEqual([], empty,Routes['league'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['league'], data=params)
        result ={"league_id": None,
                 "failures": ['Invalid league name'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['league'] +
                         " POST: request with missing parameter"
                         )
        # testing a league name parameter
        params = {'league_name':1}
        rv = self.app.post(Routes['league'], data=params)
        result = {"league_id": None,
                  "failures": ['Invalid league name'],
                  "message": "Failed to properly supply the required fields",
                  "success": False
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         " POST: request with invalid league_name"
                         )
        # proper insertion with post
        self.addLeague()
        # test a get with league
        rv = self.app.get(Routes['league'])
        result = [{'league_id': 1,'league_name':"Monday & Wedneday"}]
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(result, loads(rv.data), Routes['league'] + 
                         " GET: Failed to return list of leagues")

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
                 "failures": ['Missing color'],
                 "message": "Failed to properly supply the required fields",
                 "success": False
                }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['team']
                         + " POST: request with missing parameter"
                         )
        # testing a all invalid parameters
        params = {'color': 1,
                  'sponsor_id': 1,
                  'league_id': 1}
        rv = self.app.post(Routes['team'], data=params)
        result = {"team_id": None,
                  "failures": ['Invalid color',
                               'Invalid sponsor ID',
                               'Invalid league ID'
                               ], 
                  "message": "Failed to properly supply the required fields", 
                  "success": False
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # testing with all valid parameters
        self.addSponsor()
        self.addLeague()
        params = {'color':"Black",
                  'sponsor_id': 1,
                  'league_id': 1}
        rv = self.app.post(Routes['team'], data=params)
        result = {"team_id": 1,
                  "failures": [], 
                  "message": "", 
                  "success": True
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
 
        # test a get with team
        rv = self.app.get(Routes['team'])
        expect = [
                  {
                   'team_id': 1,
                   'color': "Black",
                   'sponsor_id': 1,
                   'league_id': 1}
                ]
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
        data = {'team_id': 1,
                'color': 'Green',
                'sponsor_id': 1,
                'league_id': None}
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
        result = {'message': 'Not a valid team ID', 'success': False}
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
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/2', data=params)
        expect = {'failures': [], 'message': 'Not a valid team ID',
                  'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid team ID")
        # invalid parameters
        params = {
                  'sponsor_id': 2,
                  'league_id': 2,
                  'color': 1}
        rv = self.app.put(Routes['team'] + '/1', data=params)
        expect = {  'failures': [
                               'Invalid color',
                               'Invalid sponsor ID',
                               'Invalid league ID'
                               ],
                    'message': 'Failed to properly supply the required fields',
                    'success': False}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid parameters")
        # successful update
        self.addSponsors()
        self.addLeagues()
        # valid update
        params = {
                  'sponsor_id': 2,
                  'league_id': 2,
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/1', data=params)
        expect = {'failures': [], 'message': '',
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
        expect = {'failures': ['Invalid home team ID',
                               'Invalid away team ID',
                               'Invalid time & date',
                               
                               'Invalid league ID'],
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
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params)
        expect = {'failures': [ 'Invalid home team ID',
                                'Invalid away team ID',
                                'Invalid time & date',
                                'Invalid league ID'],
                  'game_id': None,
                  'message': 'Failed to properly supply the required fields',
                  'success': False
                 }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")
        # test valid parameters
        self.addTeams()
        self.addLeague()
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-01", 
                  'time': "23:59",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params)
        expect = {'failures': [],
                  'game_id': 1,
                  'message': '',
                  'success': True
                 }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")
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
                'date': '2014-08-23 11:37',
                'game_id': 1,
                'home_team_id': 1,
                'league_id': 1}
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
        expect = {'message': 'Not a valid game ID', 'success': False}
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
        self.addGames()
        # invalid game id
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'league_id': 2
                 }
        rv = self.app.put(Routes['game'] + "/3", data=params)
        expect = {'failures': [], 'message': 'Invalid game ID',
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
        expect = {'failures': ['Invalid home team ID',
                               'Invalid away team ID',
                               'Invalid time & date'],
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
                  'league_id': 2
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params)
        expect = {'failures': [], 'message': '',
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