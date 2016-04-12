'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest
from api.helper import loads
from api.routes import Routes
from api.credentials import ADMIN, PASSWORD, KIK, KIKPW
from base64 import b64encode
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' + KIKPW, "utf-8")).decode("ascii")
}
from api.BaseTest import TestSetup

class GameTest(TestSetup):
    def testPost(self):
        # No games
        rv = self.app.post(Routes['vgame'])
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")
        self.addBats()
        # just monday and wednesday
        rv = self.app.post(Routes['vgame'], data={"league_id": 1})
        expect = [   {   'away_bats': [],
                        'away_score': 0,
                        'away_team': {   'captain': None,
                                         'color': 'Black',
                                         'espys': 0,
                                         'league_id': None,
                                         'sponsor_id': 2,
                                         'team_id': 2,
                                         'team_name': 'Chainsaw Black',
                                         'year': 2016},
                        'date': '2014-08-23 11:37',
                        'game_id': 1,
                        'home_bats': [   {   'hit': 's',
                                             'inning': 5,
                                             'name': 'Dallas Fraser',
                                             'rbi': 1},
                                         {   'hit': 'k',
                                             'inning': 5,
                                             'name': 'My Dream Girl',
                                             'rbi': 0}],
                        'home_score': 1,
                        'home_team': {   'captain': None,
                                         'color': 'Green',
                                         'espys': 0,
                                         'league_id': None,
                                         'sponsor_id': 1,
                                         'team_id': 1,
                                         'team_name': 'Domus Green',
                                         'year': 2016},
                        'league': {'league_id': 1, 'league_name': 'Monday & Wedneday'},
                        'status': ''}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")
        # no parameters
        rv = self.app.post(Routes['vgame'], data={})
        expect = [   {   'away_bats': [],
                            'away_score': 0,
                            'away_team': {   'captain': None,
                                             'color': 'Black',
                                             'espys': 0,
                                             'league_id': None,
                                             'sponsor_id': 2,
                                             'team_id': 2,
                                             'team_name': 'Chainsaw Black',
                                             'year': 2016},
                            'date': '2014-08-23 11:37',
                            'game_id': 1,
                            'home_bats': [   {   'hit': 's',
                                                 'inning': 5,
                                                 'name': 'Dallas Fraser',
                                                 'rbi': 1},
                                             {   'hit': 'k',
                                                 'inning': 5,
                                                 'name': 'My Dream Girl',
                                                 'rbi': 0}],
                            'home_score': 1,
                            'home_team': {   'captain': None,
                                             'color': 'Green',
                                             'espys': 0,
                                             'league_id': None,
                                             'sponsor_id': 1,
                                             'team_id': 1,
                                             'team_name': 'Domus Green',
                                             'year': 2016},
                            'league': {'league_id': 1, 'league_name': 'Monday & Wedneday'},
                            'status': ''},
                        {   'away_bats': [],
                            'away_score': 0,
                            'away_team': {   'captain': None,
                                             'color': 'Black',
                                             'espys': 0,
                                             'league_id': None,
                                             'sponsor_id': 2,
                                             'team_id': 2,
                                             'team_name': 'Chainsaw Black',
                                             'year': 2016},
                            'date': '2014-08-23 11:37',
                            'game_id': 2,
                            'home_bats': [   {   'hit': 's',
                                                 'inning': 5,
                                                 'name': 'Dallas Fraser',
                                                 'rbi': 1},
                                             {   'hit': 'k',
                                                 'inning': 5,
                                                 'name': 'My Dream Girl',
                                                 'rbi': 0}],
                            'home_score': 1,
                            'home_team': {   'captain': None,
                                             'color': 'Green',
                                             'espys': 0,
                                             'league_id': None,
                                             'sponsor_id': 1,
                                             'team_id': 1,
                                             'team_name': 'Domus Green',
                                             'year': 2016},
                            'league': {'league_id': 2, 'league_name': 'Tuesday & Thursday'},
                            'status': ''}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: View of Game")

class PlayerTest(TestSetup):
    def testPost(self):
        # no date
        rv = self.app.post(Routes['vplayer'])
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Player")
        self.addBats()
        # no parameters
        rv = self.app.post(Routes['vplayer'])
        expect = {   'Dallas Fraser': {   'avg': 1.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 1,
                                         'k': 0,
                                         'rbi': 1,
                                         's': 1,
                                         'ss': 0},
                    'My Dream Girl': {   'avg': 0.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 2,
                                         'k': 1,
                                         'rbi': 1,
                                         's': 0,
                                         'ss': 0}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Player")

    def testPostParameters(self):
        self.addBunchBats()
        rv = self.app.post(Routes['vplayer'])
        expect = {   'Dallas Fraser': {   'avg': 1.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 1,
                                         'k': 0,
                                         'rbi': 1,
                                         's': 1,
                                         'ss': 0},
                    'My Dream Girl': {   'avg': 0.0,
                                         'bats': 2,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 2,
                                         'k': 2,
                                         'rbi': 2,
                                         's': 0,
                                         'ss': 0}}
        
        self.output(loads(rv.data))
        self.output(expect)
        
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Player")
        # filter based on league
        rv = self.app.post(Routes['vplayer'], data={'league_id': 1})
        expect = {   'Dallas Fraser': {   'avg': 1.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 1,
                                         'k': 0,
                                         'rbi': 1,
                                         's': 1,
                                         'ss': 0}}

        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Player")
        # filter based on team
        rv = self.app.post(Routes['vplayer'], data={'team_id': 1})
        expect = {   'Dallas Fraser': {   'avg': 1.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 1,
                                         'k': 0,
                                         'rbi': 1,
                                         's': 1,
                                         'ss': 0},
                    'My Dream Girl': {   'avg': 0.0,
                                         'bats': 1,
                                         'd': 0,
                                         'e': 0,
                                         'fc': 0,
                                         'fo': 0,
                                         'go': 0,
                                         'hr': 0,
                                         'id': 2,
                                         'k': 1,
                                         'rbi': 1,
                                         's': 0,
                                         'ss': 0}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vplayer'] + " Post: View of Player")

class TeamTest(TestSetup):
    def estPostNoParameters(self):
        rv = self.app.post(Routes['vteam'])
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        self.addSeason()
        rv = self.app.post(Routes['vteam'])
        expect = {   '1': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'name': 'Domus Green',
                             'runs_against': 4,
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1},
                    '2': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'name': 'Sentry Sky Blue',
                             'runs_against': 4,
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1},
                    '3': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'name': 'Nightschool Navy',
                             'runs_against': 4,
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1},
                    '4': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'name': 'Brick Blue',
                             'runs_against': 4,
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1}}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")

    def testParameters(self):
        expect = {   '1': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'runs_against': 4,
                             'name': 'Domus Green',
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1},
                    '2': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'name': 'Sentry Sky Blue',
                             'runs_against': 4,
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1}}
        self.addSeason()
        rv = self.app.post(Routes['vteam'], data={'league_id': 1})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        expect = {   '1': {   'games': 3,
                             'hits_allowed': 3,
                             'hits_for': 3,
                             'losses': 1,
                             'runs_against': 4,
                             'name': 'Domus Green',
                             'runs_for': 4,
                             'ties': 1,
                             'wins': 1}}
        rv = self.app.post(Routes['vteam'], data={'team_id': 1})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")

class testPlayerLookup(TestSetup):
    def testMain(self):
        self.addPlayers()
        # players email
        expect = [   {   'email': 'fras2560@mylaurier.ca',
                            'gender': 'm',
                            'player_id': 1,
                            'player_name': 'Dallas Fraser'}]
        rv = self.app.post(Routes['vplayerLookup'], data={'email': 'fras2560@mylaurier.ca'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        # players name
        expect = [   {   'email': 'fras2560@mylaurier.ca',
                        'gender': 'm',
                        'player_id': 1,
                        'player_name': 'Dallas Fraser'}]
        rv = self.app.post(Routes['vplayerLookup'], data={'player_name': 'Dallas'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        # not a player
        expect = []
        rv = self.app.post(Routes['vplayerLookup'], data={'player_name': 'XX'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")

class TestTeamRoster(TestSetup):
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
        self.assertEqual(400, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")
        # invalid combination
        query = "?player_id=2"
        rv = self.app.delete(Routes['team_roster'] + "/1" + query)
        expect = {'message': 'Player was not a member of the team'}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")
        self.assertEqual(440, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")
        
        # proper deletion
        query = "?player_id=1"
        rv = self.app.delete(Routes['team_roster'] + "/1" + query)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")

    def testGet(self):
        #empty get
        rv = self.app.get(Routes['team_roster'] + "/1")
        expect = 'Team not found'
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on empty set")
        self.addPlayersToTeam()
        # get one team
        rv = self.app.get(Routes['team_roster'] + "/1")
        expect =  {   'captain': {   'email': 'fras2560@mylaurier.ca',
                   'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'},
                    'color': 'Green',
                    'espys': 0,
                    'league_id': None,
                    'players': [   {   'email': 'fras2560@mylaurier.ca',
                                       'gender': 'm',
                                       'player_id': 1,
                                       'player_name': 'Dallas Fraser'}],
                    'sponsor_id': 1,
                    'team_id': 1,
                    'team_name': 'Domus Green',
                    'year': 2016}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on non-empty set")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()