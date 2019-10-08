'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced team roster APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.model import Team, Player
from api.errors import TeamDoesNotExist, PlayerNotOnTeam, PlayerDoesNotExist
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, KIK, KIKPW,\
    INVALID_ID, SUCCESSFUL_DELETE_CODE


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
