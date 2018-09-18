'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest
import logging
from datetime import date
from api.helper import loads
from api.routes import Routes
from api.model import Player
from base64 import b64encode
from api.errors import TeamDoesNotExist, PlayerNotOnTeam, InvalidField,\
                    SponsorDoesNotExist, LeagueDoesNotExist
from api.advanced.import_team import TeamList
from api.advanced.import_league import LeagueList
from api.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW, INVALID_ID
import datetime

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' +
                                                  KIKPW, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


class GameTest(TestSetup):

    def testPostYear(self):
        """Test the year parameter"""
        # test an invalid year
        MockLeague(self)
        rv = self.app.post(Routes['vgame'], data={"year": INVALID_YEAR})
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: invalid year")

        # test a valid year
        rv = self.app.post(Routes['vgame'], data={"year": VALID_YEAR})
        expect = 3
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(3,
                         len(loads(rv.data)),
                         Routes['vgame'] + " Post: valid year")

    def testPostLeagueId(self):
        """Test league id parameter"""
        # test an invalid league id
        mocker = MockLeague(self)
        rv = self.app.post(Routes['vgame'], data={"league_id": INVALID_ID})
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: invalid league id")

        # test a valid league id
        data = {"league_id": mocker.get_league()['league_id']}
        rv = self.app.post(Routes['vgame'], data=data)
        expect = 3
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, len(loads(rv.data)),
                         Routes['vgame'] + " Post: valid league id")

    def testPostGameId(self):
        """Test game id parameter"""
        # test an invalid league id
        mocker = MockLeague(self)
        rv = self.app.post(Routes['vgame'], data={"game_id": INVALID_ID})
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vgame'] + " Post: invalid game id")

        # test a valid league id
        data = {"game_id": mocker.get_games()[0]['game_id']}
        rv = self.app.post(Routes['vgame'], data=data)
        games_data = loads(rv.data)
        game_data = games_data[0]
        expect = 1
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, len(games_data))
        self.assertEqual(6, game_data['away_score'])
        self.assertEqual(4, len(game_data['away_bats']))
        self.assertEqual(1, game_data['home_score'])
        self.assertEqual(4, len(game_data['home_bats']))
        self.assertLeagueModelEqual(mocker.get_league(), game_data['league'])


class PlayerTest(TestSetup):

    def testPostPlayerId(self):
        """Test player id parameter"""
        mocker = MockLeague(self)

        # test an invalid player id
        rv = self.app.post(Routes['vplayer'], data={'player_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid player id")

        # test an valid player id
        player_id = mocker.get_players()[0]['player_id']
        rv = self.app.post(Routes['vplayer'], data={"player_id": player_id})
        expect = {'Test Player 1': {'avg': 0.5,
                                    'bats': 2,
                                    'd': 0,
                                    'e': 0,
                                    'fc': 0,
                                    'fo': 0,
                                    'go': 0,
                                    'hr': 1,
                                    'id': player_id,
                                    'k': 1,
                                    'rbi': 2,
                                    's': 0,
                                    'ss': 0}}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: valid player id")

    def testPostYear(self):
        MockLeague(self)

        # test an invalid year
        rv = self.app.post(Routes['vplayer'], data={'year': INVALID_YEAR})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid year")

        # test an valid year
        rv = self.app.post(Routes['vplayer'], data={"year": VALID_YEAR})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vplayer'] + " Post: valid year")

    def testPostLeagueId(self):
        mocker = MockLeague(self)

        # test an invalid league id
        rv = self.app.post(Routes['vplayer'], data={'league_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid league id")

        # test an valid league id
        league_id = mocker.get_league()['league_id']
        expect = {'avg': 0.5,
                  'bats': 2,
                  'd': 0,
                  'e': 0,
                  'fc': 0,
                  'fo': 0,
                  'go': 0,
                  'hr': 1,
                  'id': mocker.get_players()[0]['player_id'],
                  'k': 1,
                  'rbi': 2,
                  's': 0,
                  'ss': 0}
        player_check = mocker.get_players()[0]
        rv = self.app.post(Routes['vplayer'], data={"league_id": league_id})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) == 4,
                        Routes['vplayer'] + " Post: valid league id")
        self.assertEqual(loads(rv.data)[player_check['player_name']],
                         expect,
                         Routes['vplayer'] + " Post: valid league id")

    def testPostTeamId(self):
        mocker = MockLeague(self)

        # test an invalid team id
        rv = self.app.post(Routes['vplayer'], data={'team_id': INVALID_ID})
        expect = {}
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayer'] + " Post: invalid team id")

        # test an valid team id
        team_id = mocker.get_teams()[0]['team_id']
        expect = {'avg': 0.5,
                  'bats': 2,
                  'd': 0,
                  'e': 0,
                  'fc': 0,
                  'fo': 0,
                  'go': 0,
                  'hr': 1,
                  'id': mocker.get_players()[0]['player_id'],
                  'k': 1,
                  'rbi': 2,
                  's': 0,
                  'ss': 0}
        player_check = mocker.get_players()[0]
        rv = self.app.post(Routes['vplayer'], data={"team_id": team_id})
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data).keys()) == 2,
                        Routes['vplayer'] + " Post: valid team id")
        self.assertEqual(loads(rv.data)[player_check['player_name']],
                         expect,
                         Routes['vplayer'] + " Post: valid team id")
        absent_player_name = mocker.get_players()[2]['player_name']
        player_present = absent_player_name in loads(rv.data).keys()
        self.assertTrue(not player_present,
                        Routes['vplayer'] + " Post: valid team id")


class TeamTest(TestSetup):
    def testPostTeamId(self):
        mocker = MockLeague(self)

        # invalid team id
        rv = self.app.post(Routes['vteam'], data={'team_id': INVALID_ID})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid team id")

        # valid team id
        team_id = mocker.get_teams()[0]['team_id']
        rv = self.app.post(Routes['vteam'], data={'team_id': team_id})
        expect = {'games': 3,
                  'hits_allowed': 3,
                  'hits_for': 2,
                  'losses': 1,
                  'name': 'Advanced Test Sponsor Test Team',
                  'runs_against': 6,
                  'runs_for': 1,
                  'ties': 0,
                  'wins': 0}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) == 1,
                        Routes['vteam'] + " Post: valid team id")
        self.assertEqual(expect, loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid team id")

    def testPostYear(self):
        mocker = MockLeague(self)

        # invalid year
        rv = self.app.post(Routes['vteam'], data={'year': INVALID_YEAR})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid year")

        # valid year
        team_id = mocker.get_teams()[0]['team_id']
        rv = self.app.post(Routes['vteam'], data={'year': VALID_YEAR})
        expect = {'games': 1,
                  'hits_allowed': 3,
                  'hits_for': 2,
                  'losses': 1,
                  'name': 'Advanced Test Sponsor Test Team',
                  'runs_against': 6,
                  'runs_for': 1,
                  'ties': 0,
                  'wins': 0}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vteam'] + " Post: valid year")
        self.assertEqual(expect,
                         loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid year")

    def testLeagueId(self):
        mocker = MockLeague(self)

        # invalid league id
        rv = self.app.post(Routes['vteam'], data={'league_id': INVALID_ID})
        expect = {}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: invalid league id")

        # valid league id
        league_id = mocker.get_league()['league_id']
        team_id = mocker.get_teams()[1]['team_id']
        rv = self.app.post(Routes['vteam'], data={'league_id': league_id})
        expect = {'games': 1,
                  'hits_allowed': 2,
                  'hits_for': 3,
                  'losses': 0,
                  'name': 'Advanced Test Sponsor Test Team 2',
                  'runs_against': 1,
                  'runs_for': 6,
                  'ties': 0,
                  'wins': 1}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertTrue(len(loads(rv.data).keys()) > 0,
                        Routes['vteam'] + " Post: valid year")
        self.assertEqual(expect,
                         loads(rv.data)[str(team_id)],
                         Routes['vteam'] + " Post: valid year")


class testPlayerLookup(TestSetup):
    def testMain(self):
        self.addPlayers()
        # players email
        expect = [{
                   'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'}]
        rv = self.app.post(Routes['vplayerLookup'],
                           data={'email': 'fras2560@mylaurier.ca'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: View of Team")
        # players name
        expect = [{'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'}]
        rv = self.app.post(Routes['vplayerLookup'],
                           data={'player_name': 'Dallas'})
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: View of Team")
        # only want active players
        expect = [{'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'}]
        params = {"player_name": "Dallas", "active": 1}
        rv = self.app.post(Routes['vplayerLookup'], data=params)
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
        # not an active player
        Player.query.get(1).active = False
        expect = []
        params = {"player_name": "Dallas", "active": 1}
        rv = self.app.post(Routes['vplayerLookup'], data=params)
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: View of Team")
        # not an active player but dont care
        Player.query.get(1).active = False
        expect = [{'gender': 'm',
                   'player_id': 1,
                   'player_name': 'Dallas Fraser'}]
        params = {"player_name": "Dallas", "active": 0}
        rv = self.app.post(Routes['vplayerLookup'], data=params)
        self.output(loads(rv.data), )
        self.output(expect)
        self.assertEqual(expect, loads(rv.data),
                         Routes['vteam'] + " Post: View of Team")


class TestTeamRoster(TestSetup):
    def testPost(self):
        # invalid update
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
        # add player to team
        self.addPlayersToTeam()
        # missing data
        rv = self.app.delete(Routes['team_roster'] + "/2")
        message = 'Missing required parameter in the JSON body or the post body or the query string'
        expect = {'message': {'player_id': message}}
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
        # empty get
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
        expect = {'captain': {
                  'gender': 'm',
                  'player_id': 1,
                  'player_name': 'Dallas Fraser'},
                  'color': 'Green',
                  'espys': 0,
                  'league_id': None,
                  'players': [{
                               'gender': 'm',
                               'player_id': 1,
                               'player_name': 'Dallas Fraser'}],
                  'sponsor_id': 1,
                  'team_id': 1,
                  'team_name': 'Domus Green',
                  'year': date.today().year}
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
        expect = [{'captain': {'gender': 'm',
                               'player_id': 1,
                               'player_name': 'Dallas Fraser'},
                   'color': 'Green',
                   'espys': 0,
                   'league_id': None,
                   'sponsor_id': 1,
                   'team_id': 1,
                   'team_name': 'Domus Green',
                   'year': date.today().year}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vplayerteamLookup'] +
                         " View: on Dallas Fraser")
        params = {"player_name": "NotFuckingReal"}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vplayerteamLookup'] +
                         " View: on no one")
        params = {"player_id": 1}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': {'gender': 'm',
                               'player_id': 1,
                               'player_name': 'Dallas Fraser'},
                   'color': 'Green',
                   'espys': 0,
                   'league_id': None,
                   'sponsor_id': 1,
                   'team_id': 1,
                   'team_name': 'Domus Green',
                   'year': date.today().year}]
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
        expect = [{'hits': 3,
                   'id': 3,
                   'name': 'My Dream Girl',
                   'team': 'Sentry Sky Blue',
                   'team_id': 2},
                  {'hits': 3,
                   'id': 3,
                   'name': 'My Dream Girl',
                   'team': 'Brick Blue',
                   'team_id': 4},
                  {'hits': 3,
                   'id': 2,
                   'name': 'Dallas Fraser',
                   'team': 'Domus Green',
                   'team_id': 1},
                  {'hits': 3,
                   'id': 2,
                   'name': 'Dallas Fraser',
                   'team': 'Nightschool Navy',
                   'team_id': 3}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vleagueleaders'] +
                         " View: on all years")
        params = {'stat': "hr", 'year': 2016}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        expect = [{'hits': 1,
                   'id': 2,
                   'name': 'Dallas Fraser',
                   'team': 'Domus Green',
                   'team_id': 1},
                  {'hits': 1,
                   'id': 3,
                   'name': 'My Dream Girl',
                   'team': 'Sentry Sky Blue',
                   'team_id': 2}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vleagueleaders'] +
                         " View: on 2017")


class MockLeague():
    def __init__(self, tester):
        # add a league
        self.league = tester.add_league("Advanced Test League")
        self.sponsor = tester.add_sponsor("Advanced Test Sponsor")
        self.field = "WP1"

        # add some players
        players = [("Test Player 1", "testPlayer1@mlsb.ca", "M"),
                   ("Test Player 2", "testPlayer2@mlsb.ca", "F"),
                   ("Test Player 3", "testPlayer3@mlsb.ca", "M"),
                   ("Test Player 4", "testPlayer4@mlsb.ca", "F")]
        self.players = []
        for player in players:
            self.players.append(tester.add_player(player[0],
                                                  player[1],
                                                  gender=player[2]))

        # add some teams
        teams = [("Test Team", self.sponsor, self.league),
                 ("Test Team 2", self.sponsor, self.league)]
        self.teams = []
        for team in teams:
            self.teams.append(tester.add_team(team[0],
                                              sponsor=team[1],
                                              league=self.league))

        # add the players to some teams
        tester.add_player_to_team(self.teams[0], self.players[0], captain=True)
        tester.add_player_to_team(self.teams[0], self.players[1])
        tester.add_player_to_team(self.teams[1], self.players[2])
        tester.add_player_to_team(self.teams[1], self.players[3], captain=True)

        # add some games between the teams
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        next_week = today + datetime.timedelta(days=3)
        last_week_string = week_ago.strftime("%Y-%m-%d")
        today_string = today.strftime("%Y-%m-%d")
        next_week_string = next_week.strftime("%Y-%m-%d")
        games = [(last_week_string,
                  "10:00",
                  self.teams[0],
                  self.teams[1],
                  self.league, self.field),
                 (today_string,
                  "10:00",
                  self.teams[1],
                  self.teams[0],
                  self.league, self.field),
                 (next_week_string,
                  "10:00",
                  self.teams[0],
                  self.teams[1],
                  self.league, self.field),
                 ]
        self.games = []
        for game in games:
            self.games.append(tester.add_game(game[0],
                                              game[1],
                                              game[2],
                                              game[3],
                                              game[4],
                                              field=game[5]))

        # add some bats to the games
        bats = [(self.players[0], self.teams[0], self.games[0], "K", 0),
                (self.players[0], self.teams[0], self.games[0], "HR", 1),
                (self.players[1], self.teams[0], self.games[0], "SS", 0),
                (self.players[1], self.teams[0], self.games[0], "GO", 0),
                (self.players[2], self.teams[1], self.games[0], "S", 0),
                (self.players[2], self.teams[1], self.games[0], "D", 2),
                (self.players[3], self.teams[1], self.games[0], "HR", 4),
                (self.players[3], self.teams[1], self.games[0], "GO", 0),
                ]
        self.bats = []
        for bat in bats:
            self.bats.append(tester.add_bat(bat[0],
                                            bat[1],
                                            bat[2],
                                            bat[3],
                                            rbi=bat[4]))

    def get_league(self):
        return self.league

    def get_sponsor(self):
        return self.sponsor

    def get_field(self):
        return self.field

    def get_players(self):
        return self.players

    def get_bats(self):
        return self.bats

    def get_games(self):
        return self.games

    def get_teams(self):
        return self.teams


class TestImportTeam(TestSetup):
    def testColumnsIndives(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        importer = TeamList([], logger=logger)
        try:
            importer.set_columns_indices("asd,asd,asd".split(","))
            self.assertEqual(True, False,
                             "Should have raised invalid field error")
        except InvalidField as __:
            pass
        # if it runs then should be good
        importer.set_columns_indices("Player Name,Player Email,Gender (M/F)"
                                     .split(","))
        self.assertEqual(importer.name_index, 0,
                         "Name index not set properly")
        self.assertEqual(importer.email_index, 1,
                         "Email index not set properly")
        self.assertEqual(importer.gender_index, 2,
                         "Gender index not set properly")

    def testImportHeaders(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
                 "Color:,Pink,",
                 "Captain:,Dallas Fraser,",
                 "League:,Monday & Wedneday,",
                 "Player Name,Player Email,Gender (M/F)"]
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
        self.assertEqual(importer.captain_name,
                         "Dallas Fraser",
                         "Captain name not set")
        self.assertNotEqual(importer.team, None, "Team no set properly")

    def testImportPlayers(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
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
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        lines = ["Sponsor:,Domus,",
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


class TestImportGames(TestSetup):
    TEST = [
                 "League:,Monday and Wednesday,,,",
                 "Home Team,Away Team,Date,Time,Field",
                 "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"]
    TOO_SHORT = ["Home Team,Away Team,Date,Time,Field"]
    TOO_FEW_COLUMNS = ["League:,Monday and Wednesday,,,",
                       "Home Team,Away Team,Date,Time",
                       "Domus Green,Chainsaw Black,2015-10-01", "12:00", "WP1"
                       ]
    MISSING_HOME_NAME = [
                         "League:,Monday and Wednesday,,,",
                         ",Away Team,Date,Time",
                         "Domus Green,Chainsaw Black,2015-10-01",
                         "12:00",
                         "WP1"
                            ]

    def testParseHeader(self):
        self.tl = LeagueList(TestImportGames.TEST)
        l, h = self.tl.parse_header(TestImportGames.TEST[0: 2])
        self.assertEqual(l, 'Monday and Wednesday')
        self.assertEqual(h,
                         ["Home Team", "Away Team", "Date", "Time", "Field"])

    def testCheckHeader(self):
        # check valid header
        self.tl = LeagueList(TestImportGames.TEST)
        valid = self.tl.check_header(TestImportGames.TEST[0:2])
        self.assertEqual(valid, True)
        # check a header that is too short
        self.tl = LeagueList(TestImportGames.TOO_SHORT)
        valid = self.tl.check_header(TestImportGames.TOO_SHORT[0:2])
        self.assertEqual(valid, False)
        # check a header that has too few columns
        self.tl = LeagueList(TestImportGames.TOO_FEW_COLUMNS)
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)
        # check a header that is missing a column
        self.tl = LeagueList(TestImportGames.MISSING_HOME_NAME)
        valid = self.tl.check_header(TestImportGames.TOO_FEW_COLUMNS[0:2])
        self.assertEqual(valid, False)

    def testGetLeagueID(self):
        self.addLeagues()
        self.tl = LeagueList(TestImportGames.TEST)
        team = self.tl.get_league_id("Monday & Wedneday")
        self.assertEqual(team, 1)
        self.tl = LeagueList(TestImportGames.TEST)
        try:
            team = self.tl.get_league_id("No League")
            self.assertEqual(True, False,
                             "League does not exist error should be raised")
        except Exception:
            pass

    def testImportGame(self):
        self.addTeamWithLegaue()
        # add games to the league
        self.valid_test = [
                           "League:,Monday & Wednesday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.league_id = 1
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors, [])
        # not a team in the league
        self.valid_test = [
                           "League:,Monday and Wednesday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Black,Chainsaw Black,2015-10-01,12:00, WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.league_id = 1
        self.tl.set_columns_indices(self.valid_test[1].split(","))
        self.tl.set_teams()
        self.tl.import_game(self.valid_test[2])
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(self.tl.errors,
                         ["Domus Black is not a team in the league"])

    def testValidCases(self):
        self.addTeamWithLegaue()
        # import  a set of good games
        self.valid_test = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.valid_test)
        self.tl.import_league()
        self.assertEqual([], self.tl.warnings)
        self.assertEqual([], self.tl.errors)

    def testInvalidCases(self):
        self.addTeamWithLegaue()
        # test bad header
        self.bad_header = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,sdjfkhskdj",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_header)
        self.tl.import_league()
        # test bad league
        self.bad_league = [
                           "Leaguex:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_league)
        try:
            self.tl.import_league()
        except LeagueDoesNotExist:
            pass
        # test bad game
        self.bad_game = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "Domus Green,Chainsaw Black,2015-xx-01,12:00,WP1"]
        self.tl = LeagueList(self.bad_game)
        try:
            self.tl.import_league()
            self.assertEqual(True, False, "should raise error")
        except InvalidField:
            pass
        self.bad_team = [
                           "League:,Monday & Wedneday,,,",
                           "Home Team,Away Team,Date,Time,Field",
                           "X Green,Chainsaw Black,2015-10-01,12:00,WP1"]
        # test bad team in game
        self.tl = LeagueList(self.bad_team)
        self.tl.import_league()
        self.assertEqual(self.tl.warnings, [])
        self.assertEqual(['X Green is not a team in the league'],
                         self.tl.errors)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
