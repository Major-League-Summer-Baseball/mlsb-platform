'''
@author: Dallas Fraser
@date: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest
from api.helper import loads
from api import DB
from api.routes import Routes
from api.model import Player
from datetime import datetime
from api.errors import \
    SponsorDoesNotExist, InvalidField, EspysDoesNotExist, TeamDoesNotExist,\
    PlayerDoesNotExist, NonUniqueEmail, LeagueDoesNotExist, GameDoesNotExist,\
    BatDoesNotExist
from api.credentials import ADMIN, PASSWORD
from datetime import date
from base64 import b64encode
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

from api.BaseTest import TestSetup

class TestSponsor(TestSetup):
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
        result = {'details': 'Sponsor - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['sponsor']
                         + " POST: POST request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['sponsor']
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
        self.assertEqual(rv.status_code, 201, Routes['player'] +
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
        self.addSponsors()
        # invalid sponsor
        rv = self.app.get(Routes['sponsor']+ "/999")
        expect = {'details': 999, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " Get: Invalid Sponsor")
        self.assertEqual(SponsorDoesNotExist.status_code, rv.status_code,
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
        self.addSponsors()
        # delete of invalid sponsor id
        rv = self.app.delete(Routes['sponsor'] + "/999", headers=headers)
        result = {'details': 999, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data),result,
                         Routes['sponsor'] + " DELETE Invalid Sponsor id ")
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
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
        self.addSponsors()
        # invalid sponsor id
        params = {'sponsor_name': 'New League'}
        rv = self.app.put(Routes['sponsor'] + '/999', data=params, headers=headers)
        expect = {'details': 999, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        self.assertEqual(SponsorDoesNotExist.status_code, rv.status_code,
                         Routes['sponsor'] + " PUT: given invalid sponsor ID")
        # invalid parameters
        params = {'sponsor_name': 1}
        rv = self.app.put(Routes['sponsor'] + '/1', data=params, headers=headers)
        expect = {'details': 'Sponsor - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['sponsor'] + " PUT: given invalid parameters")
        self.assertEqual(InvalidField.status_code, rv.status_code,
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

class TestEspys(TestSetup):
    def testEspysApiGet(self):
        # proper insertion
        self.addEspys()
        # invalid player id
        rv = self.app.get(Routes['espy'] + "/100")
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET invalid espy id")
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + " GET invalid espy id")
        # valid user
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        rv = self.app.get(Routes['espy'] + "/1")
        result = {   'date': d,
                    'description': 'Kik transaction',
                    'espy_id': 1,
                    'points': 1.0,
                    'receipt': None,
                    'sponsor': None,
                    'team': 'Domus Green',
                    'time': t}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET valid espy id")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET valid player id")
        rv = self.app.get(Routes['espy'] + "/2")
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        result = {   'date': d,
                    'description': 'Purchase',
                    'espy_id': 2,
                    'points': 2.0,
                    'receipt': '12019209129',
                    'sponsor': 'Domus',
                    'team': 'Chainsaw Black',
                    'time': t}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " GET valid espy id")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET valid player id")

    def testEspysApiDelete(self):
        # proper insertion with post
        self.addEspys()
        # delete of invalid espy id
        rv = self.app.delete(Routes['espy'] + "/100", headers=headers)
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " DELETE Invalid espy id ")
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + " DELETE Invalid espy id ")
        rv = self.app.delete(Routes['espy'] + "/1", headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' DELETE Valid espy id')
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         ' DELETE Valid espy id')

    def testEspysApiPut(self):
        # must add a espy
        self.addEspys()
        # invalid espy id
        params = {'team_id':1,
                  'sponsor_id':1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/100', data=params, headers=headers)
        result = {'details': 100, 'message': EspysDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid espy ID')
        self.assertEqual(rv.status_code, EspysDoesNotExist.status_code,
                         Routes['espy'] + ' PUT: Invalid espy ID')
        # invalid team id
        params = {'team_id':100,
                  'sponsor_id':1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = {'details': 100, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid espy team')
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['player'] + ' PUT: Invalid espy team')
        # invalid sponsor id
        params = {'team_id':1,
                  'sponsor_id':100,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = {'details': 100, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Invalid sponsor for Espy')
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['espy'] +' PUT: Invalid sponsor Espy')
        # successfully update
        params = {'team_id':1,
                  'sponsor_id':1,
                  'description': "Transaction",
                  'points': 10,
                  'receipt': "212309"}
        rv = self.app.put(Routes['espy'] + '/1', data=params, headers=headers)
        result = None
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         ' PUT: Valid espy update')
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         ' PUT: Valid espy update')

    def testEspysApiPost(self):
        # test an empty get
        rv = self.app.get(Routes['espy'])
        empty = loads(rv.data)
        self.assertEqual([], empty,Routes['espy'] +
                         " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200, Routes['espy'] +
                         " GET: did not return empty list")
        # missing parameters
        params = {}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        result = {   'message': { 
                                 'points': message,
                                 'team_id': message
                                 }
                  }
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result , Routes['espy'] +
                         " POST: POST request with missing parameter"
                         )
        self.assertEqual(rv.status_code, 400 , Routes['espy'] +
                         " POST: POST request with missing parameter"
                         )
        # testing a team id parameter
        self.addTeams()
        params = {'team_id':100,
                  'sponsor_id':1,
                  'points': 5}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 100, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid team"
                         )
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['espy'] + " POST: POST request with invalid team"
                         )
        # testing sponsor id parameter
        params = {'team_id':1,
                  'sponsor_id':100,
                  'points': 5}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 100, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid sponsor"
                         )
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['espy'] + " POST: POST request with invalid sponsor"
                         )
        # testing points parameter
        params = {'team_id':1,
                  'sponsor_id':100,
                  'points': "XX"}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = {'details': 'Game - points', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with invalid points"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['espy'] +
                         " POST: POST request with invalid points"
                         )
        # proper insertion with post
        params = {'team_id':1,
                  'sponsor_id':1,
                  'points': 1}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['espy'] +
                         " POST: POST request with valid data"
                         )
        self.assertEqual(rv.status_code, 201, Routes['espy'] +
                         " POST: POST request with valid data"
                         )
        rv = self.app.get(Routes['espy'])
        empty = loads(rv.data)
        d = datetime.today().strftime("%Y-%m-%d")
        t = datetime.today().strftime("%H:%M")
        expect = [   {   'date': d,
                            'description': None,
                            'espy_id': 1,
                            'points': 1.0,
                            'receipt': None,
                            'sponsor': 'Domus',
                            'team': 'Domus Green',
                            'time': t}]
        self.output(empty)
        self.output(expect)
        self.assertEqual(expect, empty,Routes['espy'] +
                         " GET: did not receive espy list")

class TestPlayer(TestSetup):
    def testPlayerApiGet(self):
        # proper insertion with post
        self.addPlayers()
        # invalid player id
        rv = self.app.get(Routes['player'] + "/999")
        result = {'details': 999, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " GET invalid player id")
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['player'] +
                         " GET invalid player id")
        # valid user
        rv = self.app.get(Routes['player'] + "/1")
        result = {"player_id": 1,
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
        self.addPlayers()
        # delete of invalid player id
        rv = self.app.delete(Routes['player'] + "/999", headers=headers)
        result = {'details': 999, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " DELETE Invalid player id ")
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['player'] +
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
        self.addPlayers()
        # invalid player id
        params = {'player_name':'David Duchovny', 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/999', data=params, headers=headers)
        result = {'details': 999, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player ID')
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code,
                         Routes['player'] +
                         ' PUT: Invalid Player ID')
        # invalid player_name type
        params = {'player_name':1, 'gender':"F"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = {'details': 'Player - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player name')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         ' PUT: Invalid Player name')
        # invalid gender
        params = {'player_name':"David Duchovny", 'gender':"X"}
        rv = self.app.put(Routes['player'] + '/1', data=params, headers=headers)
        result = {'details': 'Player - gender', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Invalid Player gender')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
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
        result = {'details': 'new@mslb.ca', 'message': NonUniqueEmail.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         ' PUT: Valid player update')
        self.assertEqual(rv.status_code, NonUniqueEmail.status_code,
                         Routes['player'] +
                         ' PUT: Valid player update')

    def testPlayerListApi(self):
        # test an empty get
        rv = self.app.get(Routes['player'])
        empty = loads(rv.data)
        self.assertEqual([], empty, Routes['player'] +
                         " GET: did not return empty list")
        self.assertEqual(rv.status_code, 200, Routes['player'] +
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
        result = {'details': 'Player - gender', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
                         " POST: POST request with invalid gender"
                         )
        # testing player_name parameter
        params = {'player_name':1,'gender':'M', 'email': 'new@mlsb.ca'}
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        result = {'details': 'Player - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with invalid name"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['player'] +
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
        self.assertEqual(rv.status_code, 201, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        rv = self.app.get(Routes['player'])
        empty = loads(rv.data)
        expect = [{
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
        result = {'details': 'fras2560@mylaurier.ca',
                  'message': NonUniqueEmail.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['player'] +
                         " POST: POST request with valid data"
                         )
        self.assertEqual(rv.status_code, NonUniqueEmail.status_code,
                         Routes['player'] +
                         " POST: POST request with valid data"
                         )

class TestLeague(TestSetup):
    def testLeagueAPIGet(self):
        # proper insertion with post
        self.addLeagues()
        # invalid league id
        rv = self.app.get(Routes['league'] + "/999")
        expect = {'details': 999, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['league'] +
                         " GET invalid league id")
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code,
                         Routes['league'] +
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
        self.addLeagues()
        # delete of invalid league id
        rv = self.app.delete(Routes['league'] + "/999", headers=headers)
        result = {'details': 999, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league']+
                         " DELETE Invalid league id ")
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code,
                         Routes['league']+
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
        self.addLeagues()
        # invalid league id
        params = {'league_name':'Chainsaw Classic'}
        rv = self.app.put(Routes['league'] + '/999', data=params, headers=headers)
        result = {'details': 999, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         ' PUT: Invalid league ID')
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code, Routes['league'] + 
                         ' PUT: Invalid league ID')
        # invalid league_name type
        params = {'league_name':1}
        rv = self.app.put(Routes['league'] + '/1', data=params, headers=headers)
        result = {'details': 'League - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         ' PUT: Invalid parameters')
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['league'] + 
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
        result = {'details': 'League - name', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         " POST: request with invalid league_name"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['league'] + 
                         " POST: request with invalid league_name"
                         )
        # proper insertion with post
        params = {'league_name':"Monday & Wednesday"}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        result = 1
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         " POST: request with valid league_name"
                         )
        self.assertEqual(rv.status_code, 201, Routes['league'] + 
                         " POST: request with valid league_name"
                         )
        params = {'league_name':"Tuesday & Thursday"}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        result = 2
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['league'] + 
                         " POST: request with valid league_name"
                         )
        self.assertEqual(rv.status_code, 201, Routes['league'] + 
                         " POST: request with valid league_name"
                         )
        # test a get with league
        rv = self.app.get(Routes['league'])
        result = [   {'league_id': 1, 'league_name': 'Monday & Wednesday'},
                     {'league_id': 2, 'league_name': 'Tuesday & Thursday'}]
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(result, loads(rv.data), Routes['league'] + 
                         " GET: Failed to return list of leagues")
        self.assertEqual(200, rv.status_code, Routes['league'] + 
                         " GET: Failed to return list of leagues")

class TestTeam(TestSetup):
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
        self.addSponsors()
        self.addLeagues()
        # testing a all invalid color
        params = {'color': 1,
                  'sponsor_id': 1,
                  'league_id': 1,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 'Team - color', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid sponsor
        params = {'color': "Green",
                  'sponsor_id': 999,
                  'league_id': 1,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 999, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code,
                         Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid league
        params = {'color': "Green",
                  'sponsor_id': 1,
                  'league_id': 999,
                  'year': 2015}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 999, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, LeagueDoesNotExist.status_code,
                         Routes['team']
                         + " POST: request with invalid parameters"
                         )
        # test invalid year
        params = {'color': "Green",
                  'sponsor_id': 1,
                  'league_id': 1,
                  'year': -1}
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        result = {'details': 'Team - year', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team']
                         + " POST: request with invalid parameters"
                         )
        self.assertEqual(rv.status_code, InvalidField.status_code,
                         Routes['team']
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
        self.assertEqual(rv.status_code, 201, Routes['team']
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
        self.addTeams()
        # test invalid team id
        rv = self.app.get(Routes['team'] + "/999")
        expect = {'details': 999, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['team'] +
                         " GET: invalid team id")
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['team'] +
                         " GET: invalid team id")
        # test valid team id
        rv = self.app.get(Routes['team'] + "/1")
        expect = {'team_id': 1,
                  'espys': 0,
                  'color': 'Green',
                  'sponsor_id': 1,
                  'league_id': None,
                  'year': date.today().year,
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
        self.addTeams()
        # delete of invalid team id
        rv = self.app.delete(Routes['team'] + "/999", headers=headers)
        result = {'details': 999, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(result)
        self.assertEqual(loads(rv.data), result, Routes['team'] +
                         " DELETE: Invalid team id ")
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code,
                         Routes['team'] +
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
        self.addTeams()
        self.addLeagues()
        # invalid team id
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': "Black",
                  'year': 2015}
        rv = self.app.put(Routes['team'] + '/999', data=params, headers=headers)
        expect = {'details': 999, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid team ID")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid team ID")
        # invalid sponsor_id
        params = {'sponsor_id': 999,
                  'league_id': 1,
                  'color': "Black",
                  'year': 2015}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'details': 999, 'message': SponsorDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(SponsorDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid sponsor")
        # invalid league_id
        params = {'sponsor_id': 1,
                  'league_id': 999,
                  'color': "Black",
                  'year': 2015}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'details': 999, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid sponsor")
        self.assertEqual(LeagueDoesNotExist.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid league")
        # invalid color
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': 1,
                  'year': 2015}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'details': 'Team - color', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid color")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid color")
        # invalid year
        params = {'sponsor_id': 1,
                  'league_id': 1,
                  'color': "Black",
                  'year': -1}
        rv = self.app.put(Routes['team'] + '/1', data=params, headers=headers)
        expect = {'details': 'Team - year', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['team'] + " PUT: given invalid year")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['team'] + " PUT: given invalid year")
        # successful update
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

class TestGame(TestSetup):
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
        self.addLeagues()
        # testing invalid date
        params = {
                  'home_team_id': 1,
                  'away_team_id': 2,
                  'date': "2014-02-2014", 
                  'time': "22:40",
                  'league_id': 1
                              }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid date")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['game']
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
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid time")
        self.assertEqual(InvalidField.status_code, rv.status_code, Routes['game']
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
        expect = {'details': 99, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid home team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, Routes['game']
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
        expect = {'details': 99, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " POST: request with invalid away team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, Routes['game']
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
        self.addGames()
        # invalid id
        rv = self.app.get(Routes['game'] + "/999")
        expect = {'details': 999, 'message': GameDoesNotExist.message}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect, loads(rv.data), Routes['game']
                         + " GET: with invalid game id")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code,
                         Routes['game']
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
        self.addGames()
        # delete invalid game id
        rv = self.app.delete(Routes['game'] + "/999", headers=headers)
        expect = {'details': 999, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['game'] + 
                         " DELETE: on invalid game id")
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code,
                         Routes['game'] + 
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
        rv = self.app.put(Routes['game'] + "/999", data=params, headers=headers)
        expect = {'details': 999, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid game id")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code,
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
        expect = {'details': 99, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid home team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
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
        expect = {'details': 99, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid away team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
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
        expect = {'details': 99, 'message': LeagueDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid league")
        self.assertEqual(LeagueDoesNotExist.status_code, rv.status_code,
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
        expect = {'details': 'Game - date', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid date")
        self.assertEqual(InvalidField.status_code, rv.status_code,
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
        expect = {'details': 'Game - time', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid time")
        self.assertEqual(InvalidField.status_code, rv.status_code,
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
        expect = {'details': 'Game - status', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid status")
        self.assertEqual(InvalidField.status_code, rv.status_code,
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
        expect = {'details': 'Game - field', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['game'] + " PUT: invalid field")
        self.assertEqual(InvalidField.status_code, rv.status_code,
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

class TestBat(TestSetup):
    def testBatList(self):
        # test an empty get
        self.addGames()
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
        expect = {'details': 99, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid player")
        self.assertEqual(PlayerDoesNotExist.status_code, rv.status_code,
                         Routes['bat']
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
        expect = {'details': 99, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid game")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code, Routes['bat']
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
        expect = {'details': '99', 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, Routes['bat']
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
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid rbi")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat']
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
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid inning")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat']
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
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['bat']
                         + " POST: request with invalid hit")
        self.assertEqual(InvalidField.status_code, rv.status_code,
                         Routes['bat']
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
        self.assertEqual(201, rv.status_code, Routes['bat']
                         + " POST: request with proper parameters")

    def testBatGet(self):
        # proper insertion of get
        self.addBats()
        # get on invalid id
        rv = self.app.get(Routes['bat']+ "/999")
        expect = {'details': 999, 'message': BatDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " GET: invalid bat id")
        self.assertEqual(rv.status_code, BatDoesNotExist.status_code,
                         Routes['bat']
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
        self.addBats()
        # delete invalid id
        rv = self.app.delete(Routes['bat']+ "/999", headers=headers)
        expect = {'details': 999, 'message': BatDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, Routes['bat']
                         + " DELETE: invalid bat id")
        self.assertEqual(rv.status_code, BatDoesNotExist.status_code,
                         Routes['bat']
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
        expect = {'details': 3, 'message': BatDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid Bat id")
        self.assertEqual(BatDoesNotExist.status_code, rv.status_code, 
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
        expect = {'details': -1, 'message': GameDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid game")
        self.assertEqual(GameDoesNotExist.status_code, rv.status_code, 
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
        expect = {'details': -1, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid player")
        self.assertEqual(PlayerDoesNotExist.status_code, rv.status_code, 
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
        expect = {'details': '-1', 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid team")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, 
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
        expect = {'details': 'Bat - rbi', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid rbi")
        self.assertEqual(InvalidField.status_code, rv.status_code, 
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
        expect = {'details': 'Bat - hit', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid hit")
        self.assertEqual(InvalidField.status_code, rv.status_code, 
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
        expect = {'details': 'Bat - inning', 'message': InvalidField.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), 
                         Routes['bat'] + " PUT: invalid inning")
        self.assertEqual(InvalidField.status_code, rv.status_code, 
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()