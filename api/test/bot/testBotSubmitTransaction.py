'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the bot upcoming games APIs
'''
from api.helper import loads
from api.routes import Routes
from api.model import Team
from base64 import b64encode
from api.test.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID,\
    addGame, SUCCESSFUL_GET_CODE
from api.errors import PlayerDoesNotExist, SponsorDoesNotExist,\
    TeamDoesNotExist, PlayerNotOnTeam
import uuid
import datetime
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}

NON_EXISTENT_SPONSOR = "FUCKINGDOESNOTEXIST"


class testSubmitTransaction(TestSetup):

    def testMain(self):
        # add some background
        sponsor = self.add_sponsor(str(uuid.uuid1()))
        league = self.add_league(str(uuid.uuid1()))
        team = self.add_team(str(uuid.uuid1()), sponsor=sponsor, league=league)
        name = str(uuid.uuid1())
        player = self.add_player(name,
                                 name + "@mlsb.ca",
                                 "m")
        route = Routes['bottransaction']

        # player does not exists
        data = {"player_id": INVALID_ID,
                "sponsor": sponsor['sponsor_name'],
                "team_id": team['team_id'],
                "amount": 1}
        expect = {'details': INVALID_ID,
                  'message': PlayerDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: transaction for non-existent player"
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # sponsor does not exist
        data = {
            "player_id": player['player_id'],
            "sponsor": NON_EXISTENT_SPONSOR,
            "team_id": team['team_id'],
            "amount": 1
        }
        expect = {'details': NON_EXISTENT_SPONSOR,
                  'message': SponsorDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: sponsor does not exist"
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # team does not exist
        data = {"player_id": player['player_id'],
                "sponsor": sponsor['sponsor_name'],
                "team_id": INVALID_ID,
                "amount": 1}
        expect = {'details': INVALID_ID,
                  'message': TeamDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: transaction for non-existent team"
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # player not on team
        data = {"player_id": player['player_id'],
                "sponsor": sponsor['sponsor_name'],
                "team_id": team['team_id'],
                "amount": 1}
        expect = {'details': player['player_id'],
                  'message': PlayerNotOnTeam.message}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: transaction player not on team"
        self.assertEqual(rv.status_code, PlayerNotOnTeam.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        self.add_player_to_team(team, player, captain=True)

        data = {"player_id": player['player_id'],
                "sponsor": sponsor['sponsor_name'],
                "team_id": team['team_id'],
                "amount": 1}
        rv = self.app.post(route, data=data, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: successful espy transaction player"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, m)
