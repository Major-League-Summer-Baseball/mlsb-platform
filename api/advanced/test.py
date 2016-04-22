'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest
import logging
from api.helper import loads
from api.routes import Routes
from api.credentials import ADMIN, PASSWORD, KIK, KIKPW
from base64 import b64encode
from api.errors import TeamDoesNotExist, PlayerNotOnTeam
from api.advanced.import_team import TeamList
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
    def testPostNoParameters(self):
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
        expect = [   {  
                            'gender': 'm',
                            'player_id': 1,
                            'player_name': 'Dallas Fraser'}]
        rv = self.app.post(Routes['vplayerLookup'], data={'email': 'fras2560@mylaurier.ca'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                 Routes['vteam'] + " Post: View of Team")
        # players name
        expect = [   {  'gender': 'm',
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
        expect = {'details': 1, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: invalid data")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, 
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
        self.assertEqual(201, rv.status_code, 
                         Routes['team_roster'] + " PUT: invalid data")
        # add a captain
        params = {"player_id": 2, "captain": 1}
        rv = self.app.post(Routes['team_roster'] + "/1", data=params)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: proper data")
        self.assertEqual(201, rv.status_code, 
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
        expect = {'details': 2, 'message': PlayerNotOnTeam.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " DELETE: Invalid combination")
        self.assertEqual(PlayerNotOnTeam.status_code, rv.status_code, 
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
        expect = {'details': 1, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: team dne")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code, 
                         Routes['team_roster'] + " GET: team dne")
        self.addPlayersToTeam()
        # get one team
        rv = self.app.get(Routes['team_roster'] + "/1")
        expect =  {   'captain': {
                   'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'},
                    'color': 'Green',
                    'espys': 0,
                    'league_id': None,
                    'players': [   {   
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

class TestFun(TestSetup):
    def testPost(self):
        self.addFun()
        params = {'year': 2012}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = [{'count': 377, 'year': 2012}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vfun'] +
                         " View: on 2012 year")
        params = {}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = [  
                    {'count': 89, 'year': 2002},
                    {'count': 100, 'year': 2003},
                    {'count': 177, 'year': 2004},
                    {'count': 186, 'year': 2005},
                    {'count': 176, 'year': 2006},
                    {'count': 254, 'year': 2007},
                    {'count': 290, 'year': 2008},
                    {'count': 342, 'year': 2009},
                    {'count': 304, 'year': 2010},
                    {'count': 377, 'year': 2011},
                    {'count': 377, 'year': 2012},
                    {'count': 461, 'year': 2013},
                    {'count': 349, 'year': 2014},
                    {'count': 501, 'year': 2015}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vfun'] +
                         " View: on 2012 year")

class TestPlayerTeamLookup(TestSetup):
    def testPost(self):
        self.addPlayersToTeam()
        params = {'player_name': "Dallas Fraser"}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [   {   'captain': {   'gender': 'm',
                       'player_id': 1,
                       'player_name': 'Dallas Fraser'},
                        'color': 'Green',
                        'espys': 0,
                        'league_id': None,
                        'sponsor_id': 1,
                        'team_id': 1,
                        'team_name': 'Domus Green',
                        'year': 2016}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vplayerteamLookup'] +
                         " View: on Dallas Fraser")
        params = {"player_name": "NotFuckingReal"}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vplayerteamLookup'] +
                         " View: on no one")


class TestLeagueLeaders(TestSetup):
    def testMain(self):
        
        # fuck this test isnt great since 
        self.mockLeaders()
        params = {'stat': "hr"}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        expect = [  {'hits': 3, 'id': 3, 'name': 'My Dream Girl', 'team': 'Sentry Sky Blue'},
                    {'hits': 3, 'id': 3, 'name': 'My Dream Girl', 'team': 'Brick Blue'},
                    {'hits': 3, 'id': 2, 'name': 'Dallas Fraser', 'team': 'Domus Green'},
                    {'hits': 3, 'id': 2, 'name': 'Dallas Fraser', 'team': 'Nightschool Navy'}
                ]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vleagueleaders'] +
                         " View: on all years")
        params = {'stat': "hr", 'year': 2016}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        expect = [  {'hits': 1, 'id': 2, 'name': 'Dallas Fraser', 'team': 'Domus Green'},
                    {'hits': 1, 'id': 3, 'name': 'My Dream Girl', 'team': 'Sentry Sky Blue'}]

        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vleagueleaders'] +
                         " View: on 2016")

class TestImportTeam(TestSetup):
    def testColumnsIndives(self):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        importer = TeamList([], logger=logger)
        try:
            importer.set_columns_indices("asd,asd,asd".split(","))
            self.assertEqual(True, False, "Should have raised invalid field error")
        except InvalidField as __:
            pass
        # if it runs then should be good
        importer.set_columns_indices("Player Name,Player Email,Gender (M/F)".split(","))
        self.assertEqual(importer.name_index, 0, "Name index not set properly")
        self.assertEqual(importer.email_index, 1, "Email index not set properly")
        self.assertEqual(importer.gender_index, 2, "Gender index not set properly")

    def testImportHeaders(self):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = [   "Sponsor:,Domus,",
                    "Color:,Pink,",
                    "Captain:,Dallas Fraser,",
                    "League:,Monday & Wedneday,",
                    "Player Name,Player Email,Gender (M/F)",]
        importer = TeamList(lines, logger=logger)
        # test a invalid sponsor
        try:
            importer.import_headers()
            self.assertEqual(True, False, "Sponsor does not exist")
        except SponsorDoesNotExist as __:
            pass
        self.addSponsors()
        importer = TeamList(lines, logger=logger)
        # test a invalid league
        try:
            importer.import_headers()
            self.assertEqual(True, False, "League does not exist")
        except LeagueDoesNotExist as __:
            pass
        self.addLeagues()
        importer.import_headers()
        self.assertEqual(importer.captain_name, "Dallas Fraser", "Captain name not set")
        self.assertNotEqual(importer.team, None, "Team no set properly")

    def testImportPlayers(self):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = [   "Sponsor:,Domus,",
                    "Color:,Pink,",
                    "Captain:,Dallas Fraser,",
                    "League:,Monday & Wedneday,",
                    "Player Name,Player Email,Gender (M/F)"
                    "Laura Visentin,vise3090@mylaurier.ca,F",
                    "Dallas Fraser,fras2560@mylaurier.ca,M",
                    "Mitchell Ellul,ellu6790@mylaurier.ca,M",
                    "Mitchell Ortofsky,orto2010@mylaurier.ca,M",
                    "Adam Shaver,shav3740@mylaurier.ca,M",
                    "Taylor Takamatsu,taka9680@mylaurier.ca,F",
                    "Jordan Cross,cros7940@mylaurier.ca,M",
                    "Erin Niepage,niep3130@mylaurier.ca,F",
                    "Alex Diakun,diak1670@mylaurier.ca,M",
                    "Kevin Holmes,holm4430@mylaurier.ca,M",
                    "Kevin McGaire,kevinmcgaire@gmail.com,M",
                    "Kyle Morrison,morr1090@mylaurier.ca,M",
                    "Ryan Lackey,lack8060@mylaurier.ca,M",
                    "Rory Landy,land4610@mylaurier.ca,M",
                    "Claudia Vanderholst,vand6580@mylaurier.ca,F",
                    "Luke MacKenzie,mack7980@mylaurier.ca,M",
                    "Jaron Wu,wuxx9824@mylaurier.ca,M",
                    "Tea Galli,gall2590@mylaurier.ca,F",
                    "Cara Hueston ,hues8510@mylaurier.ca,F",
                    "Derek Schoenmakers,scho8430@mylaurier.ca,M",
                    "Marni Shankman,shan3500@mylaurier.ca,F",
                    "Christie MacLeod ,macl5230@mylaurier.ca,F"
                    ]
        importer = TeamList(lines, logger=logger)
        # mock the first half
        self.addTeams()
        importer.team = self.teams[0]
        importer.captain_name = "Dakkas Fraser"
        importer.email_index = 1
        importer.name_index = 0
        importer.gender_index = 2
        # if no errors are raised then golden
        importer.import_players(5)

    def testAddTeam(self):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = [   "Sponsor:,Domus,",
                    "Color:,Pink,",
                    "Captain:,Dallas Fraser,",
                    "League:,Monday & Wedneday,",
                    "Player Name,Player Email,Gender (M/F)"
                    "Laura Visentin,vise3090@mylaurier.ca,F",
                    "Dallas Fraser,fras2560@mylaurier.ca,M",
                    "Mitchell Ellul,ellu6790@mylaurier.ca,M",
                    "Mitchell Ortofsky,orto2010@mylaurier.ca,M",
                    "Adam Shaver,shav3740@mylaurier.ca,M",
                    "Taylor Takamatsu,taka9680@mylaurier.ca,F",
                    "Jordan Cross,cros7940@mylaurier.ca,M",
                    "Erin Niepage,niep3130@mylaurier.ca,F",
                    "Alex Diakun,diak1670@mylaurier.ca,M",
                    "Kevin Holmes,holm4430@mylaurier.ca,M",
                    "Kevin McGaire,kevinmcgaire@gmail.com,M",
                    "Kyle Morrison,morr1090@mylaurier.ca,M",
                    "Ryan Lackey,lack8060@mylaurier.ca,M",
                    "Rory Landy,land4610@mylaurier.ca,M",
                    "Claudia Vanderholst,vand6580@mylaurier.ca,F",
                    "Luke MacKenzie,mack7980@mylaurier.ca,M",
                    "Jaron Wu,wuxx9824@mylaurier.ca,M",
                    "Tea Galli,gall2590@mylaurier.ca,F",
                    "Cara Hueston ,hues8510@mylaurier.ca,F",
                    "Derek Schoenmakers,scho8430@mylaurier.ca,M",
                    "Marni Shankman,shan3500@mylaurier.ca,F",
                    "Christie MacLeod ,macl5230@mylaurier.ca,F"
                    ]
        importer = TeamList(lines, logger=logger)
        self.addLeagues()
        self.addSponsors()
        # no point checking for errors that were tested above
        importer.add_team()
        self.assertEqual(importer.warnings, ['Team was created'],
                         "Should be no warnings")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()