'''
@author: Dallas Fraser
@author: 2015-08-25
@organization: MLSB API
@summary: Tests all the basic APIs
'''
from api import app
import unittest
import tempfile
from api.helper import loads
from api import DB
from pprint import PrettyPrinter
from api.routes import Routes
from api.model import Player, Team, Sponsor, League, Game, Bat
from api.errors import IFSC, NUESC, SDNESC, LDNESC, TDNESC, PDNESC, GDNESC
from api.credentials import ADMIN, PASSWORD
from base64 import b64encode
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = "2014-8-23"
        self.t = "11:37"
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
        DB.create_all()

    def tearDown(self):
        DB.session.commit()
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

    def addAnotherSponsor(self):
        self.sponsor = Sponsor("Chainsaw")
        DB.session.add(self.sponsor)
        DB.session.commit()
        self.assertEqual(self.sponsor.id, 2, "Could not add sponsor")

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
        self.game = Game(self.d,
                         self.t,
                         self.teams[0].id,
                         self.teams[1].id,
                         self.league.id)
        DB.session.add(self.game)
        DB.session.commit()
        self.assertEqual(1, self.game.id)

    def addGames(self):
        self.addTeams()
        self.addLeagues()
        self.games = [Game(self.d,
                           self.t,
                           self.teams[0].id,
                           self.teams[1].id,
                           self.leagues[0].id),
                      Game(self.d,
                           self.t,
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
    
    def addBats(self):
        self.addGames()
        self.bats = [Bat(self.players[0].id,
                       self.teams[0].id,
                       self.games[0].id,
                       "S",
                       5,
                       
                       rbi=1),
                     Bat(self.players[1].id,
                         self.teams[0].id,
                         self.games[1].id,
                         "K",
                         5)
                     ]
        for i in range(0, len(self.bats)):
            DB.session.add(self.bats[i])
        DB.session.commit()

    def addCaptainToTeam(self):
        self.addTeam()
        team = Team.query.get(1)
        team.insert_player(1, captain=True)
    
    def addPlayersToTeam(self):
        self.addTeams()
        team = Team.query.get(1)
        team.insert_player(1, captain=True)
        team.insert_player(2, captain=False)
        DB.session.commit()

class TestSponsor(BaseTest):
    def testSponsorListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['sponsor'])
        empty = loads(rv.data)
        self.assertEqual([], empty,"/sponsors GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        result = {'message': {'sponsor_name': message}
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['sponsor']
                         + " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400, Routes['sponsor']
                         + " POST: POST request with invalid parameters"
                         )        
        # testing with improper name parameters
        params = {'sponsor_name':1,}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        result = {'message': 'Invalid name for Sponsor'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['sponsor']
                         + " POST: POST request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['sponsor']
                         + " POST: POST request with invalid parameters"
                         )
        # proper insertion with post
        params = {'sponsor_name':"Domus"}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        self.assertEqual(rv.status_code, 200, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        # test a get with sponsors
        rv = self.app.get(Routes['sponsor'])
        result = [   {  'sponsor_id': 1,
                        'sponsor_name': 'Domus',
                        'link': None,
                        'description': None}
                 ]
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(result, loads(rv.data), Routes['sponsor']
                         + " GET Failed to return list of tournaments")
        self.assertEqual(200, rv.status_code, Routes['sponsor']
                         + " GET Failed to return list of tournaments")

    def testSponsorAPIGet(self):
        # proper insertion with post
        self.addSponsor()
        # invalid sponsor
        rv = self.app.get(Routes['sponsor']+ "/2")
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " Get: Invalid Sponsor")
        self.assertEqual(404, rv.status_code,
                         Routes['sponsor'] + " Get: Invalid Sponsor")
        # valid sponsor
        rv = self.app.get(Routes['sponsor']+ "/1")
        expect = { 'sponsor_id': 1,
                 'sponsor_name': 'Domus',
                 'link': None,
                 'description': None}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " Get: Valid Sponsor")
        self.assertEqual(200, rv.status_code,
                         Routes['sponsor'] + " Get: valid Sponsor")

    def testSponsorAPIDelete(self):
        # proper insertion with post
        self.addSponsor()
        # delete of invalid sponsor id
        rv = self.app.delete(Routes['sponsor'] + "/2", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result,
                         Routes['sponsor'] + " DELETE Invalid Sponsor id ")
        self.assertEqual(rv.status_code, 404,
                         Routes['sponsor'] + " DELETE Invalid Sponsor id ")
        # delete valid sponsor id
        rv = self.app.delete(Routes['sponsor'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result,
                         Routes['sponsor'] + ' DELETE Valid sponsor id')
        self.assertEqual(rv.status_code, 200,
                         Routes['sponsor'] + " DELETE valid Sponsor id ")

    def testSponsorAPIPut(self):
        # proper insertion with post
        self.addSponsor()
        # invalid sponsor id
        params = {'sponsor_name': 'New League'}
        rv = self.app.put(Routes['sponsor'] + '/2', data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        self.assertEqual(404, rv.status_code,
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        # invalid parameters
        params = {'sponsor_name': 1}
        rv = self.app.put(Routes['sponsor'] + '/1', data=params, headers=headers)
        expect = {'message': 'Invalid name for Sponsor'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid parameters")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['sponsor'] + " PUT: given invalid parameters")
        #successful update
        params = {'sponsor_name': 'New League'}
        rv = self.app.put(Routes['sponsor'] + '/1', data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")
        self.assertEqual(200, rv.status_code,
                         Routes['sponsor'] + " PUT: Failed to update Sponsor")

class TestPlayer(BaseTest):
    def testPlayerApiGet(self):
        # proper insertion with post
        self.addPlayer()
        # invalid player id
        rv = self.app.get(Routes['player'] + "/2")
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " GET invalid player id")
        self.assertEqual(rv.status_code, 404, Routes['player'] +
                         " GET invalid player id")
        # valid user
        rv = self.app.get(Routes['player'] + "/1")
        result = {"player_id": 1,
                  'email': 'fras2560@mylaurier.ca',
                  'gender': 'm',
                  'player_name': 'Dallas Fraser'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " GET valid player id")
        self.assertEqual(rv.status_code, 200, Routes['player'] +
                         " GET valid player id")

    def testPlayerApiDelete(self):
        # proper insertion with post
        self.addPlayer()
        # delete of invalid player id
        rv = self.app.delete(Routes['player'] + "/2", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " DELETE Invalid player id ")
        self.assertEqual(rv.status_code, 404, Routes['player'] +
                         " DELETE Invalid player id ")
        rv = self.app.delete(Routes['player'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' DELETE Valid player id')
        self.assertEqual(rv.status_code, 200, Routes['player'] +
                         ' DELETE Valid player id')

    def testPlayerApiPut(self):
        # must add a player
        self.addPlayer()
        # invalid player id
        params = {'player_name':'David Duchovny', 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/2', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player ID')
        self.assertEqual(rv.status_code, 404, Routes['player'] +
                         ' PUT: Invalid Player ID')
        # invalid player_name type
        params = {'player_name':1, 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = {'message': 'Invalid name for Player'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player name')
        self.assertEqual(rv.status_code, IFSC, Routes['player'] +
                         ' PUT: Invalid Player name')
        # invalid gender
        params = {'player_name':"David Duchovny", 'gender':"X"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = {'message': 'Invalid gender for Player'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player gender')
        self.assertEqual(rv.status_code, IFSC, Routes['player'] +
                         ' PUT: Invalid Player gender')
        # successfully update
        params = {'player_name':"David Duchovny", 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Valid player update')
        self.assertEqual(rv.status_code, 200, Routes['player'] +
                         ' PUT: Valid player update')
        # duplicate email
        p = Player("first player", "new@mslb.ca")
        DB.session.add(p)
        DB.session.commit()
        params = {'player_name':"David Duchovny", 'email':"new@mslb.ca"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = {'message': 'Email was a duplicate new@mslb.ca'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Valid player update')
        self.assertEqual(rv.status_code, NUESC, Routes['player'] +
                         ' PUT: Valid player update')

    def testPlayerListApi(self):
        # test an empty get
        rv = self.app.get(Routes['player'])
        empty = loads(rv.data)
        self.assertEqual([], empty,Routes['player'] +
                         " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200,Routes['player'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        result = {   'message': { 
                                 'player_name': message,
                                 'email': message
                                 }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['player'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400 , Routes['player'] +
                         " POST: POST request with missing parameter"
                         )
        # testing a gender parameter
        params = {'player_name':'Dallas Fraser',
                  'gender':'X',
                  'email': "new@mlsb.ca"}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'message': 'Invalid gender for Player'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        # testing player_name parameter
        params = {'player_name':1,'gender':'M', 'email': 'new@mlsb.ca'}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'message': 'Invalid name for Player'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid name"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['player'] +
                         " POST: POST request with invalid name"
                         )
        # proper insertion with post
        params = {'player_name':"Dallas Fraser",
                  "gender": "M",
                  "email": "fras2560@mylaurier.ca",
                  "password":"Suck it"}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        self.assertEqual(rv.status_code, 200, Routes['player'] +
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
        # duplicate email
        params = {'player_name':"Copy cat",
                  "gender": "M",
                  "email": "fras2560@mylaurier.ca",
                  "password":"Suck it"}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'message': 'Email is a duplicate - fras2560@mylaurier.ca'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        self.assertEqual(rv.status_code, NUESC, Routes['player'] +
                         " POST: POST request with valid data"
                         )

class TestLeague(BaseTest):
    def testLeagueAPIGet(self):
        # proper insertion with post
        self.addLeague()
        # invalid league id
        rv = self.app.get(Routes['league'] + "/2")
        self.output(loads(rv.data))
        self.assertEqual(loads(rv.data), None, Routes['league'] +
                         " GET invalid league id")
        self.assertEqual(rv.status_code, 404, Routes['league'] +
                         " GET invalid league id")
        # valid league id
        rv = self.app.get(Routes['league'] + "/1")
        result = {'league_id': 1, 'league_name': 'Monday & Wedneday'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result,Routes['league'] +
                         " GET valid league id")
        self.assertEqual(rv.status_code, 200,Routes['league'] +
                         " GET valid league id")

    def testLeagueAPIDelete(self):
        # proper insertion with post
        self.addLeague()
        # delete of invalid league id
        rv = self.app.delete(Routes['league'] + "/2", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league']+
                         " DELETE Invalid league id ")
        self.assertEqual(rv.status_code, 404, Routes['league']+
                         " DELETE Invalid league id ")
        rv = self.app.delete(Routes['league'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] +
                         ' DELETE Valid league id')
        self.assertEqual(rv.status_code, 200, Routes['league'] +
                         ' DELETE Valid league id')
        

    def testLeagueAPIPut(self):
        # must add a League
        self.addLeague()
        # invalid league id
        params = {'league_name':'Chainsaw Classic'}
        rv = self.app.put(Routes['league'] + '/2', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         ' PUT: Invalid league ID')
        self.assertEqual(rv.status_code, 404, Routes['league'] + 
                         ' PUT: Invalid league ID')
        # invalid league_name type
        params = {'league_name':1}
        rv = self.app.put(Routes['league'] + '/1', data=params, headers=headers)
        result = {'message': 'Invalid name for League'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         ' PUT: Invalid parameters')
        self.assertEqual(rv.status_code, IFSC, Routes['league'] + 
                         ' PUT: Invalid parameters')
        # successfully update
        params = {'league_name':"Chainsaw Classic"}
        rv = self.app.put(Routes['league'] + '/1', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         ' PUT: Successful Update')
        self.assertEqual(rv.status_code, 200, Routes['league'] + 
                         ' PUT: Successful Update')

    def testLeagueListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['league'])
        empty = loads(rv.data)
        self.assertEqual([], empty, Routes['league'] +
                         " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200, Routes['league'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        result = {   'message': {
                                 'league_name': message
                                 }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['league'] +
                         " POST: request with missing parameter"
                         )
        self.assertEqual(loads(rv.data), result , Routes['league'] +
                         " POST: request with missing parameter"
                         )
        # testing a league name parameter
        params = {'league_name':1}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        result = {'message': 'Invalid name for League'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         " POST: request with invalid league_name"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['league'] + 
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
        self.assertEqual(200, rv.status_code, Routes['league'] + 
                         " GET: Failed to return list of leagues")

class TestTeam(BaseTest):
    def testTeamListAPI(self):
        # test an empty get
        rv = self.app.get(Routes['team'])
        empty = loads(rv.data)
        self.assertEqual([], empty,
                         Routes['team'] + " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200,
                         Routes['team'] + " GET: did not return empty list")
        
        # missing parameters
        params = {}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        result ={   'message': {
                                'color': message,
                                'league_id': message,
                                'sponsor_id': message,
                                'year': message}
                 }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['team']
                         + " POST: request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400 , Routes['team']
                         + " POST: request with missing parameter"
                         )
        self.addSponsor()
        self.addLeague()
        # testing a all invalid color
        params = {'color': 1,
                  'sponsor_id': 1,
                  'league_id': 1,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'message': 'Invalid color for Team'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid sponsor
        params = {'color': "Green",
                  'sponsor_id': 999,
                  'league_id': 1,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'message': 'Sponsor does not Exist 999'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, SDNESC, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid league
        params = {'color': "Green",
                  'sponsor_id': 1,
                  'league_id': 999,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'message': 'League does not Exist 999'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, LDNESC, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid year
        params = {'color': "Green",
                  'sponsor_id': 1,
                  'league_id': 1,
                  'year': -1}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'message': 'Invalid year for Team'}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, IFSC, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # testing with all valid parameters
        params = {'color':"Black",
                  'sponsor_id': 1,
                  'league_id': 1,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, 200, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test a get with team
        rv = self.app.get(Routes['team'])
        expect = [   {  'captain': None,
                        'color': 'Black',
                        'espys': 0,
                        'league_id': 1,
                        'sponsor_id': 1,
                        'team_id': 1,
                        'team_name': 'Domus Black',
                        'year': 2015}
                  ]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team']
                         + " GET: Failed to return list of teams")
        self.assertEqual(200, rv.status_code, Routes['team']
                         + " GET: Failed to return list of teams")

    def testTeamGet(self):
        # proper insertion with post
        self.addTeam()
        # test invalid team id
        rv = self.app.get(Routes['team'] + "/2")
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " GET: invalid team id")
        self.assertEqual(rv.status_code, 404, Routes['team'] +
                         " GET: invalid team id")
        # test valid team id
        rv = self.app.get(Routes['team'] + "/1")
        expect = {'team_id': 1,
                  'espys': 0,
                  'color': 'Green',
                  'sponsor_id': 1,
                  'league_id': None,
                  'year': 2015,
                  'captain': None,
                  'team_name': 'Domus Green'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] + 
                         " GET: valid team id")
        self.assertEqual(rv.status_code, 200, Routes['team'] + 
                         " GET: valid team id")

    def testTeamDelete(self):
        # proper insertion with post
        self.addTeam()
        # delete of invalid team id
        rv = self.app.delete(Routes['team'] + "/2", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " DELETE: Invalid team id ")
        self.assertEqual(rv.status_code, 404, Routes['team'] +
                         " DELETE: Invalid team id ")
        rv = self.app.delete(Routes['team'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         ' DELETE: Valid team id')
        self.assertEqual(rv.status_code, 200, Routes['team'] +
                         ' DELETE: Valid team id')

    def testTeamPut(self):
        # proper insertion with post
        self.addTeam()
        self.addLeague()
        # invalid team id
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': "Black",
                  'year': 2015,
                  'espys': 10}
        rv = self.app.put(Routes['team'] + '/2', data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid team ID")
        self.assertEqual(404, rv.status_code,
                         Routes['team'] + " PUT: given invalid team ID")

        # invalid sponsor_id
        params = {'sponsor_id': 999,
                  'league_id': 1,
                  'color': "Black",
                  'year': 2015,
                  'espys': 10}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'message': 'Sponsor does not Exist 999'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(SDNESC, rv.status_code,
                         Routes['team'] + " PUT: given invalid sponsor")
        # invalid league_id
        params = {'sponsor_id': 1,
                  'league_id': 999,
                  'color': "Black",
                  'year': 2015,
                  'espys': 10}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'message': 'League does not Exist 999'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(LDNESC, rv.status_code,
                         Routes['team'] + " PUT: given invalid league")
        # invalid color
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': 1,
                  'year': 2015,
                  'espys': 10}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'message': 'Invalid color for Team'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid color")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['team'] + " PUT: given invalid color")
        # invalid year
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': "Black",
                  'year': -1,
                  'espys': 10}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'message': 'Invalid year for Team'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid year")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['team'] + " PUT: given invalid year")
        # successful update
        self.addAnotherSponsor()
        self.addLeagues()
        # valid update
        params = {
                  'sponsor_id': 2,
                  'league_id': 2,
                  'color': "Black"}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " PUT: Failed to update a team")
        self.assertEqual(rv.status_code, 200, Routes['team'] +
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
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        expect = {   'message': {   
                                 'away_team_id': message,
                                 'date': message,
                                 'home_team_id': message,
                                 'league_id': message,
                                 'time': message}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")
        self.assertEqual(400, rv.status_code, Routes['game']
                         + " POST: request with missing parameters")
        self.addTeams()
        self.addLeague()
        # testing invalid date
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-2014", 
                  'time': "22:40",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'message': 'Invalid date for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid date")
        self.assertEqual(IFSC, rv.status_code, Routes['game']
                         + " POST: request with invalid date")
        # testing invalid time
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-10", 
                  'time': "22:66",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'message': 'Invalid time for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid time")
        self.assertEqual(IFSC, rv.status_code, Routes['game']
                         + " POST: request with invalid time")
        # testing invalid home team id
        params = {
                  'home_team_id': 99,
                  'away_team_id': 2,
                  'date': "2014-02-10", 
                  'time': "22:40",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'message': 'Game does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid home team")
        self.assertEqual(TDNESC, rv.status_code, Routes['game']
                         + " POST: request with invalid home team")
        # testing invalid home team id
        params = {
                  'home_team_id': 1,
                  'away_team_id': 99,
                  'date': "2014-02-10", 
                  'time': "22:40",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'message': 'Game does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid away team")
        self.assertEqual(TDNESC, rv.status_code, Routes['game']
                         + " POST: request with invalid away team")
        # test valid parameters
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-01", 
                  'time': "23:59",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = 1
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with missing parameters")

    def testGameGet(self):
        # proper insertion
        self.addGame()
        # invalid id
        rv = self.app.get(Routes['game'] + "/2")
        expect = None
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " GET: with invalid game id")
        self.assertEqual(404, rv.status_code, Routes['game']
                         + " GET: with invalid game id")
        # valid id
        rv = self.app.get(Routes['game'] + "/1")
        expect = {'away_team_id': 2,
                  'away_team':'Chainsaw Black',
                  'date': '2014-08-23',
                  'game_id': 1,
                  'home_team_id': 1,
                  'home_team': 'Domus Green',
                  'league_id': 1,
                  'status': "",
                  'field':"",
                  'time': '11:37'}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " GET: with valid game id")
        self.assertEqual(200, rv.status_code, Routes['game']
                         + " GET: with valid game id")

    def testGameDelete(self):
        # proper insertion
        self.addGame()
        # delete invalid game id
        rv = self.app.delete(Routes['game'] + "/2", headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] + 
                         " DELETE: on invalid game id")
        self.assertEqual(rv.status_code, 404, Routes['game'] + 
                         " DELETE: on invalid game id")
        
        # delete valid game id
        rv = self.app.delete(Routes['game'] + "/1", headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] + 
                         " DELETE: on valid game id")
        self.assertEqual(rv.status_code, 200, Routes['game'] + 
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
                  'league_id': 2,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/3", data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid game id")
        self.assertEqual(404, rv.status_code,
                         Routes['game'] + " PUT: invalid game id")
        # invalid home team
        params = {
                  'home_team_id': 99,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'league_id': 2,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Team does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid home team")
        self.assertEqual(TDNESC, rv.status_code,
                         Routes['game'] + " PUT: invalid home team")
        # invalid away team
        params = {
                  'home_team_id': 2,
                  'away_team_id': 99,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'league_id': 2,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Team does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid away team")
        self.assertEqual(TDNESC, rv.status_code,
                         Routes['game'] + " PUT: invalid away team")
        # invalid league
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'league_id': 99,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'League does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid league")
        self.assertEqual(LDNESC, rv.status_code,
                         Routes['game'] + " PUT: invalid league")
        # invalid date
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "xx-08-22",
                  'time': "11:37",
                  'league_id': 1,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid date for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid date")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['game'] + " PUT: invalid date")
        # invalid time
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2015-08-22",
                  'time': "XX:37",
                  'league_id': 1,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid time for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid time")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['game'] + " PUT: invalid time")
        # invalid status
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2015-08-22",
                  'time': "12:37",
                  'league_id': 1,
                  'status': 1,
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid status for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid status")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['game'] + " PUT: invalid status")
        # invalid field
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2015-08-22",
                  'time': "12:37",
                  'league_id': 1,
                  'status': "Championship",
                  'field': 1
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid field for Game'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid field")
        self.assertEqual(IFSC, rv.status_code,
                         Routes['game'] + " PUT: invalid field")
        # valid update parameters
        params = {
                  'home_team_id': 2,
                  'away_team_id': 1,
                  'date': "2014-08-22",
                  'time': "11:37",
                  'league_id': 2,
                  'status': "Championship",
                  'field': "WP1"
                 }
        rv = self.app.put(Routes['game'] + "/1", data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: valid update")
        self.assertEqual(200, rv.status_code,
                         Routes['game'] + " PUT: valid update")

class TestBat(BaseTest):
    def testBatList(self):
        # test an empty get
        self.addGame()
        rv = self.app.get(Routes['bat'])
        empty = loads(rv.data)
        self.assertEqual([], empty,
                        Routes['bat'] + "GET: did not return empty list")
        self.assertEqual(rv.status_code, 200,
                        Routes['bat'] + "GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        expect = {   
                  'message': {
                               'game_id': message,
                               'hit': message,
                               'player_id': message,
                               'team_id': message 
                              }
                  }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with missing parameters")
        self.assertEqual(400, rv.status_code, Routes['bat']
                         + " POST: request with missing parameters")
        # testing invalid player
        params = {
                  'game_id': 1,
                  'player_id': 99,
                  'team_id': 1,
                  'rbi': 2, 
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Player does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid player")
        self.assertEqual(PDNESC, rv.status_code, Routes['bat']
                         + " POST: request with invalid player")
        # testing invalid game
        params = {
                  'game_id': 99,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 2, 
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Game does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid game")
        self.assertEqual(GDNESC, rv.status_code, Routes['bat']
                         + " POST: request with invalid game")
        # testing invalid team
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 99,
                  'rbi': 2, 
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Team does not Exist 99'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid team")
        self.assertEqual(TDNESC, rv.status_code, Routes['bat']
                         + " POST: request with invalid team")
        # testing invalid rbi
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 100, 
                  'hit': "hr",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Invalid rbi for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid rbi")
        self.assertEqual(IFSC, rv.status_code, Routes['bat']
                         + " POST: request with invalid rbi")
        # testing invalid inning
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 1, 
                  'hit': "hr",
                  'inning': -1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Invalid inning for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid inning")
        self.assertEqual(IFSC, rv.status_code, Routes['bat']
                         + " POST: request with invalid inning")
        # testing invalid hit
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 1, 
                  'hit': "xx",
                  'inning': 1
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = {'message': 'Invalid hit for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid hit")
        self.assertEqual(IFSC, rv.status_code, Routes['bat']
                         + " POST: request with invalid hit")
        # test all valid parameters
        
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'rbi': 1, 
                  'hit': "HR",
                  'team_id': 1,
                  'inning': 4
                              }
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        expect = 1
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with proper parameters")
        self.assertEqual(200, rv.status_code, Routes['bat']
                         + " POST: request with proper parameters")

    def testBatGet(self):
        # proper insertion of get
        self.addBat()
        # get on invalid id
        rv = self.app.get(Routes['bat']+ "/2")
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " GET: invalid bat id")
        self.assertEqual(rv.status_code, 404, Routes['bat']
                         + " GET: invalid bat id")
        # get on valid id
        rv = self.app.get(Routes['bat']+ "/1")
        expect = {  'bat_id': 1,
                    'game_id': 1,
                    'hit': 's',
                    'inning': 5,
                    'player': 'Dallas Fraser email:fras2560@mylaurier.ca',
                    'player_id': 1,
                    'rbi': 1,
                    'team': 'Domus Green',
                    'team_id': 1}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " GET: valid bat id")
        self.assertEqual(rv.status_code, 200, Routes['bat']
                         + " GET: valid bat id")

    def testBatDelete(self):
        # proper insertion of get
        self.addBat()
        # delete invalid id
        rv = self.app.delete(Routes['bat']+ "/2", headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " DELETE: invalid bat id")
        self.assertEqual(rv.status_code, 404, Routes['bat']
                         + " DELETE: invalid bat id")
        # delete valid id
        rv = self.app.delete(Routes['bat']+ "/1", headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " DELETE: valid bat id")
        self.assertEqual(rv.status_code, 200, Routes['bat']
                         + " DELETE: valid bat id")

    def testBatPut(self):
        # proper insertion of get
        self.addBats()
        # invalid bat ID
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/3", data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid Bat id")
        self.assertEqual(404, rv.status_code, 
                         Routes['bat'] + " PUT: invalid Bat id")
        # test invalid game_id
        params = {
                  'game_id': -1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Game does not Exist -1'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid game")
        self.assertEqual(GDNESC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid game")
        # test invalid game_id
        params = {
                  'game_id': 1,
                  'player_id': -1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Player does not Exist -1'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid player")
        self.assertEqual(PDNESC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid player")
        # test invalid game_id
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': -1,
                  'rbi': 4, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Team does not Exist -1'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid team")
        self.assertEqual(TDNESC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid team")
        # test invalid rbi
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 99, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid rbi for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid rbi")
        self.assertEqual(IFSC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid rbi")
        # test invalid hit
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "XX",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid hit for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid hit")
        self.assertEqual(IFSC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid hit")
        # test invalid inning
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "hr",
                  'inning': -1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = {'message': 'Invalid inning for Bat'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid inning")
        self.assertEqual(IFSC, rv.status_code, 
                         Routes['bat'] + " PUT: invalid inning")
        # valid update
        params = {
                  'game_id': 1,
                  'player_id': 1,
                  'team_id': 1,
                  'rbi': 4, 
                  'hit': "HR",
                  'inning': 1
                              }
        rv = self.app.put(Routes['bat'] + "/1", data=params, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: valid parameters")
        self.assertEqual(200, rv.status_code, 
                         Routes['bat'] + " PUT: valid parameters")

class TestTeamRoster(BaseTest):
    def testPost(self):
        #invalid update
        params = {"player_id": 1}
        rv = self.app.post(Routes['team_roster'] + "/1", data=params)
        expect = 'Team not found'
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: invalid data")
        self.assertEqual(404, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")
        # add player to team        
        self.addTeams()
        params = {"player_id": 1}
        rv = self.app.post(Routes['team_roster'] + "/1", data=params)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: proper data")
        self.assertEqual(200, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")
        # add a captain
        params = {"player_id": 2, "captain": 1}
        rv = self.app.post(Routes['team_roster'] + "/1", data=params)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: proper data")
        self.assertEqual(200, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")

    def testDelete(self):
        #add player to team
        self.addPlayersToTeam()
        # missing data
        rv = self.app.delete(Routes['team_roster']+"/2")
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        expect = {   'message': {   'player_id': message}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Missing header")
        # invalid combination
        query = "?player_id=2"
        rv = self.app.delete(Routes['team_roster'] + "/1" + query)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")
        # proper deletion
        query = "?player_id=2"
        rv = self.app.delete(Routes['team_roster'] + "/1" + query)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")

    def testGet(self):
        #empty get
        self.show_results = True
        rv = self.app.get(Routes['team_roster'] + "/1")
        expect = 'Team not found'
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on empty set")
        self.addPlayersToTeam()
        # get one team
        rv = self.app.get(Routes['team_roster'] + "/1")
        expect =  {   
                   'captain': {   'email': 'fras2560@mylaurier.ca',
                                           'gender': 'm',
                                           'player_id': 1,
                                           'player_name': 'Dallas Fraser'},
                    'color': 'Green',
                    'espys': 0,
                    'league_id': None,
                    'players': [   {   'email': 'dream@mylaurier.ca',
                                       'gender': 'f',
                                       'player_id': 2,
                                       'player_name': 'My Dream Girl'}],
                    'sponsor_id': 1,
                    'team_id': 1,
                    'team_name': 'Domus Green',
                    'year': 2015
                }
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on non-empty set")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()