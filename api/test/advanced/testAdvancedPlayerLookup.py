'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced player lookup APIs
'''
from datetime import date
from api.helper import loads
from api.routes import Routes
from base64 import b64encode
from api.test.advanced.mock_league import MockLeague
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}
VALID_YEAR = date.today().year
INVALID_YEAR = 100


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
        print("sdfdskfhds")
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
        print("Hello sdfsd")
        rv = self.app.post(Routes['vplayerLookup'], data={'active': active,
                                                          'player_name': name})
        expect = []
        self.output(expect)
        self.output(loads(rv.data))
        activity = [_player['active'] for _player in loads(rv.data)]
        error_message = Routes['vplayerLookup'] + ":non-active player returned"
        self.assertTrue(False not in activity, error_message)
        self.assertEqual(expect, loads(rv.data), error_message)
