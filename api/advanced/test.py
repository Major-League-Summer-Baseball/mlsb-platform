'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the basic APIs
'''
import unittest

from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.model import Team, Player
from api.errors import TeamDoesNotExist, PlayerNotOnTeam, PlayerDoesNotExist
from api.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW, INVALID_ID,\
                         SUCCESSFUL_DELETE_CODE, SUCCESSFUL_GET_CODE
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
        self.assertTrue(len(loads(rv.data)) > 0,
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
        """Test team id parameter"""
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
        """Test year parameter"""
        self.show_results = True
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
        """Test league id parameter"""
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


class PlayerLookupTest(TestSetup):
    def testPlayerName(self):
        """Test player name parameter"""
        mocker = MockLeague(self)

        # non existent player name
        expect = []
        name = "NAME DOES NOT EXISTS FOR REASONS"
        rv = self.app.post(Routes['vplayerLookup'], data={'player_name': name})
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerLookup'] + ": invalid player name")

        # a valid player
        expect = [mocker.get_players()[0]]
        name = mocker.get_players()[0]['player_name']
        rv = self.app.post(Routes['vplayerLookup'], data={'player_name': name})
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerLookup'] + ": valid player name")

    def testEmail(self):
        """Test email parameter"""
        mocker = MockLeague(self)

        # non existent player name
        expect = []
        email = "EMAILDOESNOTEXISTSFOR@reasons.com"
        rv = self.app.post(Routes['vplayerLookup'], data={'email': email})
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerLookup'] + ": invalid email")

        # a valid email
        expect = [mocker.get_players()[0]]
        email = mocker.get_player_email(0)
        rv = self.app.post(Routes['vplayerLookup'], data={'email': email})
        self.output(expect)
        self.output(loads(rv.data))
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerLookup'] + ": valid email")

    def testActive(self):
        """Test active parameter"""
        mocker = MockLeague(self)

        # all players
        player = mocker.get_players()[0]
        expect = [player]
        active = 0

        name = player['player_name']
        rv = self.app.post(Routes['vplayerLookup'], data={'active': active,
                                                          'player_name': name})
        self.output(expect)
        self.output(loads(rv.data))
        self.assertTrue(len(loads(rv.data)) > 0,
                        Routes['vplayerLookup'] + ": active & non-active")
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerLookup'] + ": active & non-active")

        # now make the player non-active
        self.deactivate_player(player)

        # only active players
        active = 1
        rv = self.app.post(Routes['vplayerLookup'], data={'active': active,
                                                          'player_name': name})
        expect = []
        self.output(expect)
        self.output(loads(rv.data))
        activity = [player['active'] for player in loads(rv.data)]
        error_message = Routes['vplayerLookup'] + ":non-active player returned"
        self.assertTrue(False not in activity, error_message)
        self.assertEqual(expect, loads(rv.data), error_message)


class TeamRosterTest(TestSetup):
    def testPost(self):
        """Test adding an invalid player to a team"""
        # mock leagues tests a valid post
        mocker = MockLeague(self)
        player_id = mocker.get_players()[0]['player_id']
        team_id = mocker.get_teams()[0]['team_id']

        # invalid update
        params = {"player_id": player_id}
        rv = self.app.post(Routes['team_roster'] + "/" + str(INVALID_ID),
                           data=params,
                           headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect,
                         Routes['team_roster'] + " POST: invalid data")
        self.assertEqual(TeamDoesNotExist.status_code, rv.status_code,
                         Routes['team_roster'] + " PUT: invalid data")

        # invalid player
        params = {"player_id": INVALID_ID}
        rv = self.app.post(Routes['team_roster'] + "/" + str(team_id),
                           data=params,
                           headers=headers)
        expect = {'details': INVALID_ID, 'message': PlayerDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data),
                         expect,
                         Routes['team_roster'] + " POST: invalid data")
        self.assertEqual(TeamDoesNotExist.status_code,
                         rv.status_code,
                         Routes['team_roster'] + " PUT: invalid data")

    def testDelete(self):
        """ Test deleting player from team roster"""
        # add player to team
        mocker = MockLeague(self)
        team_id = mocker.get_teams()[0]['team_id']
        player_id = mocker.get_players()[0]['player_id']
        player_two_id = mocker.get_players()[2]['player_id']

        # invalid combination
        query = "?player_id=" + str(player_two_id)
        url_request = Routes['team_roster'] + "/" + str(team_id) + query
        rv = self.app.delete(url_request, headers=headers)
        expect = {'details': player_two_id, 'message': PlayerNotOnTeam.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['team_roster'] + "DELETE: Invalid combination")
        self.assertEqual(PlayerNotOnTeam.status_code,
                         rv.status_code,
                         Routes['team_roster'] + " PUT: invalid data")

        # team does not exists
        query = "?player_id=" + str(player_id)
        url_request = Routes['team_roster'] + "/" + str(INVALID_ID) + query
        rv = self.app.delete(url_request,
                             headers=headers)
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['team_roster'] + "DELETE: Invalid player id")
        self.assertEqual(TeamDoesNotExist.status_code,
                         rv.status_code,
                         Routes['team_roster'] + " PUT: invalid player id")

        # player does not exist
        query = "?player_id=" + str(INVALID_ID)
        url_request = Routes['team_roster'] + "/" + str(team_id) + query
        rv = self.app.delete(url_request, headers=headers)
        expect = {'details': INVALID_ID, 'message': PlayerNotOnTeam.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['team_roster'] + "DELETE: Invalid player id")
        self.assertEqual(PlayerNotOnTeam.status_code,
                         rv.status_code,
                         Routes['team_roster'] + " PUT: invalid player id")

        # proper deletion
        query = "?player_id=" + str(player_id)
        url_request = Routes['team_roster'] + "/" + str(team_id) + query
        rv = self.app.delete(url_request, headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(SUCCESSFUL_DELETE_CODE,
                         rv.status_code,
                         Routes['team_roster'] + "DELETE: Invalid combination")
        self.assertEqual(expect, loads(rv.data),
                         Routes['team_roster'] + "DELETE: Invalid combination")

        # make sure player it not on team
        team = Team.query.get(team_id)
        player = Player.query.get(player_id)
        self.assertTrue(player.id not in [p.id for p in team.players],
                        Routes['team_roster'] + " DELETE: player not removed")
        self.assertTrue(player.id != team.player_id,
                        Routes['team_roster'] + " DELETE: player not removed")

    def testGet(self):
        # empty get
        rv = self.app.get(Routes['team_roster'] + "/" + str(INVALID_ID))
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['team_roster'] + " GET: team DNE")
        self.assertEqual(TeamDoesNotExist.status_code,
                         rv.status_code,
                         Routes['team_roster'] + " GET: team DNE")

        # add some teams
        mocker = MockLeague(self)
        team = mocker.get_teams()[0]
        team_id = team['team_id']
        captain = mocker.get_players()[0]
        player = mocker.get_players()[1]
        league = mocker.get_league()

        # get one team
        rv = self.app.get(Routes['team_roster'] + "/" + str(team_id))
        expect = {
                  'captain': captain,
                  'color': team['color'],
                  'espys': 0,
                  'league_id': league['league_id'],
                  'players': [
                              captain,
                              player
                              ],
                  'sponsor_id': team['sponsor_id'],
                  'team_id': team['team_id'],
                  'team_name': team['team_name'],
                  'year': date.today().year}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['team_roster'] +
                         " GET: on non-empty set")


class TestFun(TestSetup):
    def testPost(self):
        """Test fun view"""
        params = {'year': 2002}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = [{'count': 89, 'year': 2002}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data), Routes['vfun'] +
                         " View: on 2012 year")

        # get all the years
        params = {}
        rv = self.app.post(Routes['vfun'], data=params)
        expect = {'count': 89, 'year': 2002}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect, loads(rv.data)[0], Routes['vfun'] +
                         " View: on 2012 year")


class TestPlayerTeamLookup(TestSetup):
    def testEmail(self):
        """Tests using a player email as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player emails
        params = {'email': mocker.get_player_email(0)}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

    def testPlayerName(self):
        """Tests using a player name as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player names
        params = {'player_name': mocker.get_players()[0]['player_name']}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

        # test a test player names
        player_two = mocker.get_players()[3]
        team_two = mocker.get_teams()[1]
        params = {'player_name': "Test Player"}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']},
                  {'captain': player_two,
                   'color': team_two['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team_two['team_id'],
                   'team_name': team_two['team_name'],
                   'year': team_two['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])

    def testPlayerId(self):
        """Tests using a player id as a parameter"""
        mocker = MockLeague(self)
        league = mocker.get_league()
        team = mocker.get_teams()[0]
        player = mocker.get_players()[0]
        sponsor = mocker.get_sponsor()

        # test a test player names
        params = {'player_id': mocker.get_players()[0]['player_id']}
        rv = self.app.post(Routes['vplayerteamLookup'], data=params)
        expect = [{'captain': player,
                   'color': team['color'],
                   'espys': 0,
                   'league_id': league['league_id'],
                   'sponsor_id': sponsor['sponsor_id'],
                   'team_id': team['team_id'],
                   'team_name': team['team_name'],
                   'year': team['year']}]
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expect,
                         loads(rv.data),
                         Routes['vplayerteamLookup'])


class TestLeagueLeaders(TestSetup):
    def testMain(self):
        # fuck this test isnt great since
        MockLeague(self)

        params = {'stat': "hr"}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        hr_hits = loads(rv.data)
        self.output(loads(rv.data))
        error_message = Routes['vleagueleaders'] + " View: on all years"
        self.assertEqual(SUCCESSFUL_GET_CODE, rv.status_code, error_message)
        self.assertTrue(len(loads(rv.data)) > 0, error_message)

        # check the classification parameter change hits numbers
        params = {'stat': "s"}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        singles_hits = loads(rv.data)
        error_message = Routes['vleagueleaders'] + " View: on all years"
        self.assertEqual(SUCCESSFUL_GET_CODE, rv.status_code, error_message)
        self.assertNotEqual(hr_hits, singles_hits, error_message)

        # check the year parameter changes hits numbers
        params = {'stat': "hr", 'year': VALID_YEAR + 1}
        rv = self.app.post(Routes['vleagueleaders'], data=params)
        expect = []
        self.output(loads(rv.data))
        self.output(expect)
        error_message = (Routes['vleagueleaders'] +
                         " View: on {}".format(VALID_YEAR + 1))
        self.assertEqual(expect, loads(rv.data), error_message)
        self.assertNotEqual(hr_hits, loads(rv.data), error_message)


class MockLeague():
    def __init__(self, tester):
        # add a league
        self.league = tester.add_league("Advanced Test League")
        self.sponsor = tester.add_sponsor("Advanced Test Sponsor")
        self.field = "WP1"

        # add some players
        players = [("Test Player 1", "TestPlayer1@mlsb.ca", "M"),
                   ("Test Player 2", "TestPlayer2@mlsb.ca", "F"),
                   ("Test Player 3", "TestPlayer3@mlsb.ca", "M"),
                   ("Test Player 4", "TestPlayer4@mlsb.ca", "F")]
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

    def get_player_email(self, index):
        return self.players[index]['player_name'].replace(" ", "") + "@mlsb.ca"


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
