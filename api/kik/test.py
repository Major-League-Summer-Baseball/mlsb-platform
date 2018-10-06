'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Tests all the Kik APIs
'''
from api.helper import loads
from api.routes import Routes
from api.model import Espys, Team
from base64 import b64encode
from api.BaseTest import TestSetup, ADMIN, PASSWORD, INVALID_ID, VALID_YEAR,\
                         SUCCESSFUL_GET_CODE, UNAUTHORIZED, KIK, KIKPW,\
                         addGame
from api.errors import TeamDoesNotExist, NotTeamCaptain, TeamAlreadyHasCaptain,\
                       PlayerNotSubscribed, GameDoesNotExist,\
                       InvalidField, SponsorDoesNotExist, PlayerDoesNotExist
import unittest
import datetime
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}

KIK_HEADER = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' +
                                                  KIKPW, "utf-8")
                                            ).decode("ascii")
}


class testAuthenticateCaptain(TestSetup):
    def testMain(self):
        # add some background
        league = self.add_league("Test Kik Bot League")
        sponsor = self.add_sponsor("Test Kik Bot Sponsor")
        team = self.add_team("Black", sponsor, league, VALID_YEAR)
        player = self.add_player("TestKikCaptain", "testKikBot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        player = self.add_kik_to_player(player, kik)

        # valid request
        data = {'kik': kik,
                "captain": player['player_name'],
                "team": team['team_id']}
        expect = team['team_id']
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        error_message = Routes['kikcaptain'] + " POST: Authenticate Captain"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error_message)
        self.assertEqual(expect, loads(rv.data), error_message)

        # invalid team
        data = {'kik': kik,
                "captain": player['player_name'],
                "team": INVALID_ID}
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = Routes['kikcaptain'] + " POST: invalid team"
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code, message)
        self.assertEqual(expect, loads(rv.data), message)

        # captain name does not match
        data = {'kik': kik,
                "captain": "Fucker",
                "team": team['team_id']}
        expect = {'details': player['player_name'],
                  'message': NotTeamCaptain.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = Routes['kikcaptain'] + "POST: name of captain does not match"
        self.assertEqual(rv.status_code, NotTeamCaptain.status_code, message)
        self.assertEqual(expect, loads(rv.data), message)

        # if someone else tries to say captain with same name but different
        # kik name than one previously stated
        data = {'kik': "fucker",
                "captain": player['player_name'],
                "team": team['team_id']}
        expect = {'details': kik,
                  'message': TeamAlreadyHasCaptain.message}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = Routes['kikcaptain'] + " POST: sketchy shit"
        self.assertEqual(rv.status_code,
                         TeamAlreadyHasCaptain.status_code,
                         message)
        self.assertEqual(expect, loads(rv.data), message)

        # invalid credentials
        data = {'kik': "fucker", "captain": "df", "team": team['team_id']}
        rv = self.app.post(Routes['kikcaptain'], data=data, headers=headers)
        error_message = Routes['kikcaptain'] + " POST: invalid credentials"
        self.assertEqual(rv.status_code, UNAUTHORIZED, error_message)


class testSubscribe(TestSetup):
    def testMain(self):

        # add some background
        league = self.add_league("Test Kik Bot League")
        sponsor = self.add_sponsor("Test Kik Bot Sponsor")
        team = self.add_team("Black", sponsor, league, VALID_YEAR)
        player = self.add_player("TestKikCaptain", "testKikBot@mlsb.ca", "m")
        player_two = self.add_player("TestKikPlayer",
                                     "testPlayerKik@mlsb.ca",
                                     "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        kik2 = "testKikPlayer"
        route = Routes['kiksubscribe']

        # valid request
        data = {'kik': kik,
                "name": player['player_name'],
                "team": team['team_id']}
        expect = True
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = route + " POST: valid request"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, message)
        self.assertEqual(expect, loads(rv.data), message)

        # team does not exist
        data = {'kik': kik,
                "name": player['player_name'],
                "team": INVALID_ID}
        expect = {'details': INVALID_ID, 'message': TeamDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = route + " POST: team does not exist"
        self.assertEqual(rv.status_code, TeamDoesNotExist.status_code, message)
        self.assertEqual(expect, loads(rv.data), message)

        # player not on team
        data = {'kik': kik2,
                "name": player_two['player_name'],
                "team": team['team_id']}
        expect = True
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = route + " POST: player not on team"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, message)
        self.assertEqual(expect, loads(rv.data), message)

        # player already subscribed
        data = {'kik': kik,
                "name": player['player_name'],
                "team": team['team_id']}
        expect = True
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = route + " POST: already subscribed"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, message)
        self.assertEqual(expect, loads(rv.data), message)

        # check to make sure not additional points were rewarded
        espys = Espys.query.filter_by(team_id=team['team_id'])
        d = datetime.date.today().strftime("%Y-%m-%d")
        expect = [(d, 2.0),
                  (d, 0.0),
                  (d, 2.0),
                  (d, 0.0)]
        for index, espy in enumerate(espys):
            self.output(espy.json())
            self.assertEqual(espy.json()['points'], expect[index][1])
            self.assertEqual(espy.json()['date'], expect[index][0])


class testUnSubscribe(TestSetup):
    def testMain(self):
        # add some background
        league = self.add_league("Test Kik Bot League")
        sponsor = self.add_sponsor("Test Kik Bot Sponsor")
        team = self.add_team("Black", sponsor, league, VALID_YEAR)
        player = self.add_player("TestKikCaptain", "testKikBot@mlsb.ca", "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        player = self.add_kik_to_player(player, kik)
        route = Routes['kikunsubscribe']

        # player does not exist
        data = {'kik': "DoesNotExist",
                "team": team['team_id']}
        expect = {'details': 'Player is not subscribed',
                  'message': 'Player is not subscribed'}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: team does not exist"
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # unsubscribe
        data = {'kik': kik,
                "team": team['team_id']}
        expect = True
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        message = route + " POST: team does not exist"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, message)
        self.assertEqual(expect, loads(rv.data), message)


class testSubmitScores(TestSetup):
    def testMain(self):
        # add some background
        game = addGame(self)
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Kik Bot Captain",
                                 "testkikbot@mlsb.ca",
                                 "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        route = Routes['kiksubmitscore']

        # invalid captain
        data = {'kik': kik,
                'game_id': game['game_id'],
                'score': 1,
                'hr': [player['player_id']],
                'ss': []}
        expect = {'details': kik,
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: invalid kik user name"
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # add the kik name to the captain
        player = self.add_kik_to_player(player, kik)

        # invalid game
        data = {'kik': kik,
                'game_id': INVALID_ID,
                'score': 1,
                'hr': [player['player_id']],
                'ss': []}
        expect = {'details': INVALID_ID, 'message': GameDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: invalid game id"
        self.assertEqual(rv.status_code, GameDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # more hr than runs scored
        data = {'kik': kik,
                'game_id': game['game_id'],
                'score': 1,
                'hr': [player['player_id'], player['player_id']],
                'ss': []}
        expect = {'details': 'More hr than score',
                  'message': InvalidField.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: more hr than runs"
        self.assertEqual(rv.status_code, InvalidField.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # normal request
        self.submit_a_score_by_kik(kik, game, 1, hr=[player['player_id']])


class testSubmitTransaction(TestSetup):
    def testMain(self):
        # this api was not used so testing is not complete

        # add some background
        sponsor = self.add_sponsor("Test Kik Sposnor")
        game = addGame(self)
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Kik Bot Captain",
                                 "testkikbot@mlsb.ca",
                                 "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        route = Routes['kiktransaction']

        # player not subscribed
        data = {'kik': kik,
                "sponsor": sponsor['sponsor_name'],
                "amount": 1}
        expect = {'details': kik,
                  'message': PlayerNotSubscribed.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: transaction for player not subscribed"
        self.assertEqual(rv.status_code, PlayerNotSubscribed.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # subscribe the player
        player = self.add_kik_to_player(player, kik)

        # sponsor does not exist
        data = {
                'kik': kik,
                "sponsor": "FUCKINGDOESNOTEXIST",
                "amount": 1
                }
        expect = {'details': 'FUCKINGDOESNOTEXIST',
                  'message': SponsorDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " Post: sponsor does not exist"
        self.assertEqual(rv.status_code, SponsorDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)


class testCaptainGames(TestSetup):
    def testMain(self):
        # add some background
        day = datetime.date.today() - datetime.timedelta(days=1)
        game = addGame(self, day=day.strftime("%Y-%m-%d"), time="22:40")
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Kik Bot Captain",
                                 "testkikbot@mlsb.ca",
                                 "m")
        self.add_player_to_team(team, player, captain=True)
        kik = "testKikCaptain"
        route = Routes['kikcaptaingames']

        # invalid captian request
        data = {'kik': kik,
                "team": team['team_id']}
        expect = {'details': None, 'message': NotTeamCaptain.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: Invalid Captain's games"
        self.assertEqual(rv.status_code, NotTeamCaptain.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # add the kik name to the captain
        player = self.add_kik_to_player(player, kik)

        # valid request
        data = {'kik': kik,
                "team": team['team_id']}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: Valid Captain's games"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, m)
        self.assertTrue(len(loads(rv.data)) > 0, m)
        self.assertEqual(game['game_id'], loads(rv.data)[0]['game_id'], m)

        # submit score
        self.submit_a_score_by_kik(kik, game, 1, hr=[player['player_id']])

        # second valid request
        data = {'kik': kik,
                "team": team['team_id']}
        expect = []
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = Routes['kikcaptaingames'] + " POST: Invalid Captain's games"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, m)
        self.assertEqual(expect, loads(rv.data), m)


class testUpcomingGames(TestSetup):
    def testMain(self):
        # add some background
        day = datetime.date.today() + datetime.timedelta(days=1)
        game = addGame(self, day=day.strftime("%Y-%m-%d"), time="22:40")
        team_model = Team.query.get(game['home_team_id'])
        team = team_model.json()
        player = self.add_player("Test Kik Bot Captain",
                                 "testkikbot@mlsb.ca",
                                 "m")
        self.add_player_to_team(team, player, captain=True)
        route = Routes['kikupcominggames']

        # non-subscribed player
        data = {'name': 'DoesNotExist'}
        expect = {'details': 'DoesNotExist',
                  'message': PlayerDoesNotExist.message}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: Player DNE for upcoming games"
        self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code, m)
        self.assertEqual(expect, loads(rv.data), m)

        # subscribed player upcoming games
        data = {'name': player['player_name']}
        rv = self.app.post(route, data=data, headers=KIK_HEADER)
        self.output(loads(rv.data))
        self.output(expect)
        m = route + " POST: Subscribed player for upcoming games"
        self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, m)
        self.assertTrue(len(loads(rv.data)) > 0, m)
        self.assertEqual(game['game_id'], loads(rv.data)[0]['game_id'], m)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
