'''
Created on Apr 12, 2016

@author: Dallas
'''
from api import app
from api import DB
from pprint import PrettyPrinter
from api.model import Player, Team, Sponsor, League, Game, Bat, Espys, Fun
from base64 import b64encode
from datetime import date
from api.helper import loads
from api.routes import Routes
import unittest
import tempfile
import os
from api.variables import PAGE_SIZE


# environment variables
ADMIN = os.environ['ADMIN']
PASSWORD = os.environ['PASSWORD']
KIK = os.environ['KIK']
KIKPW = os.environ['KIKPW']

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD,
                                                  "utf-8")).decode("ascii")
}

KIK_HEADER = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' + KIKPW,
                                                  "utf-8")).decode("ascii")
}

SUCCESSFUL_GET_CODE = 200
SUCCESSFUL_DELETE_CODE = 200
SUCCESSFUL_PUT_CODE = 200
SUCCESSFUL_POST_CODE = 201
INVALID_ID = 10000000
UNAUTHORIZED = 401
VALID_YEAR = date.today().year


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = "2014-8-23"
        self.t = "11:37"
        self.counter = 1
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.to_delete = []
        self.bats_to_delete = []
        self.games_to_delete = []
        self.fun_to_delete = []
        self.espys_to_delete = []
        self.teams_to_delete = []
        self.players_to_delete = []
        self.sponsors_to_delete = []
        self.leagues_to_delete = []
        if (not self.tables_created()):
            DB.engine.execute('''
                                  DROP TABLE IF EXISTS fun;
                                  DROP TABLE IF EXISTS roster;
                                  DROP TABLE IF EXISTS bat;
                                  DROP TABLE IF EXISTS espys;
                                  DROP TABLE IF EXISTS game;
                                  DROP TABLE IF EXISTS team;
                                  DROP TABLE IF EXISTS player;
                                  DROP TABLE IF EXISTS sponsor;
                                  DROP TABLE IF EXISTS league;
                          ''')
            DB.create_all()

    def tearDown(self):
        to_delete = (self.delete_list(self.espys_to_delete) +
                     self.delete_list(self.bats_to_delete) +
                     self.delete_list(self.games_to_delete) +
                     self.delete_list(self.players_to_delete) +
                     self.delete_list(self.teams_to_delete) +
                     self.delete_list(self.sponsors_to_delete) +
                     self.delete_list(self.leagues_to_delete) +
                     self.delete_list(self.fun_to_delete))
        final_not_delete = self.delete_list(to_delete)
        self.assertEqual(len(final_not_delete) > 0, False,
                         "Unable to delete everying upon tear down")

    def increment_counter(self):
        """Increments the counter by 1"""
        self.counter += 1

    def get_counter(self):
        """Returns the counter used to differentiate between creates object"""
        return self.counter

    def delete_list(self, values):
        """Deletes the list of values given from the database"""
        not_deleted = []
        for item in reversed(values):
            try:
                DB.session.delete(item)
                DB.session.commit()
            except Exception as e:
                print(e)
                not_deleted.append(item)
        return not_deleted

    def tables_created(self):
        """Returns True if the tables are created"""
        # TODO figure out how to check if tables are created
        return True

    def output(self, data):
        """Prints the data if show_results is True"""
        if self.show_results:
            self.pp.pprint(data)

    def add_fun(self, count, year=date.today().year):
        """Returns a fun json object that was created with a post request"""
        params = {"year": year, "count": count}
        rv = self.app.post(Routes['fun'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add fun object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add fun object")
        fun = Fun.query.filter(Fun.year == loads(rv.data)).first()
        self.fun_to_delete.append(fun)
        return fun.json()

    def add_sponsor(self,
                    sponsor_name,
                    link=None,
                    description=None,
                    active=True,
                    nickname=None):
        """Returns a sponsor json object created with a post request"""
        active = 1 if active else 0
        params = {'sponsor_name': sponsor_name,
                  "link": link,
                  "description": description,
                  "active": active,
                  "nickname": nickname}
        rv = self.app.post(Routes['sponsor'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add sponsor object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add sponsor object")
        sponsor = Sponsor.query.get(loads(rv.data))
        self.sponsors_to_delete.append(sponsor)
        return sponsor.json()

    def add_league(self, league_name):
        """Returns a league json object that was created with a post request"""
        params = {"league_name": league_name}
        rv = self.app.post(Routes['league'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add league object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add league object")
        league = League.query.get(loads(rv.data))
        self.leagues_to_delete.append(league)
        return league.json()

    def add_player(self,
                   player_name,
                   email,
                   gender=None,
                   password='default',
                   active=True):
        """Returns a player json object that was created with a post request"""
        active = 1 if active else 0
        params = {"player_name": player_name,
                  "email": email,
                  "gender": gender,
                  "password": password,
                  "active": active
                  }
        rv = self.app.post(Routes['player'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add player object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add player object")
        player = Player.query.get(loads(rv.data))
        self.players_to_delete.append(player)
        return player.json()

    def add_team(self,
                 color,
                 sponsor=None,
                 league=None,
                 year=date.today().year):
        """Returns a team json object that was created with a post request"""
        params = {"sponsor_id": sponsor['sponsor_id'],
                  "league_id": league['league_id'],
                  "color": color,
                  "year": year
                  }
        rv = self.app.post(Routes['team'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add team object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add team object")
        team = Team.query.get(loads(rv.data))
        self.teams_to_delete.append(team)
        return team.json()

    def add_game(self,
                 date,
                 time,
                 home_team,
                 away_team,
                 league,
                 status="",
                 field=""):
        """Returns a game json object that was created with a post request"""
        params = {"home_team_id": int(home_team["team_id"]),
                  "away_team_id": int(away_team["team_id"]),
                  "date": date,
                  "time": time,
                  "league_id": int(league['league_id']),
                  "status": status
                  }
        rv = self.app.post(Routes['game'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add game object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add game object")
        game = Game.query.get(loads(rv.data))
        self.games_to_delete.append(game)
        return game.json()

    def add_bat(self, player, team, game, classification, inning=1, rbi=0):
        """Returns a bat json object that was created with a post request"""
        params = {"player_id": int(player['player_id']),
                  "rbi": rbi,
                  "inning": inning,
                  "hit": classification,
                  "team_id": int(team['team_id']),
                  "game_id": int(game["game_id"])}
        rv = self.app.post(Routes['bat'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add bat object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add bat object")
        bat = Bat.query.get(loads(rv.data))
        self.bats_to_delete.append(bat)
        return bat.json()

    def add_espys(self,
                  team,
                  sponsor,
                  description=None,
                  points=0.0,
                  receipt=None,
                  time=None,
                  date=None):
        """Returns a espy json object that was created with a post request"""
        params = {"team_id": team["team_id"],
                  "sponsor_id": sponsor["sponsor_id"],
                  "description": description,
                  "points": points,
                  "receipt": receipt,
                  "date": date,
                  "time": time}
        rv = self.app.post(Routes['espy'], data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add espy object")
        self.assertTrue(loads(rv.data) > 0, "Unable to add espy object")
        espy = Espys.query.get(loads(rv.data))
        self.espys_to_delete.append(espy)
        return espy.json()

    def add_kik_to_player(self, player, kik):
        """Adds the kik user name to the player"""
        player = DB.session.query(Player).get(player['player_id'])
        player.kik = kik
        DB.session.commit()
        return player.json()

    def add_player_to_team(self, team, player, captain=False):
        """Adds the given player to a team"""
        params = {"player_id": player['player_id']}
        if captain:
            params['captain'] = 1
        rv = self.app.post(Routes['team_roster'] + "/" + str(team['team_id']),
                           data=params, headers=headers)
        self.assertEqual(SUCCESSFUL_POST_CODE,
                         rv.status_code,
                         "Unable to add player to team")

    def remove_player_from_team(self, team, player):
        """Removes a player from a team"""
        query = "?player_id=" + str(player['player_id'])
        url_request = (Routes['team_roster'] +
                       "/" +
                       str(team['team_id']) +
                       query)
        rv = self.app.delete(url_request, headers=headers)
        self.assertEqual(SUCCESSFUL_DELETE_CODE,
                         rv.status_code,
                         "Unable to remove player to team")

    def deactivate_player(self, player):
        """Deactivate the given player"""
        p = Player.query.get(player['player_id'])
        p.deactivate()
        DB.session.commit()

    def submit_a_score(self, player, game, score, hr=[], ss=[]):
        """Submits a score and returns the list of bats created"""
        data = {'player_id': player['player_id'],
                'game_id': game['game_id'],
                'score': score,
                'hr': hr,
                'ss': ss}

        rv = self.app.post(Routes['botsubmitscore'],
                           data=data,
                           headers=headers)
        self.assertEqual(SUCCESSFUL_GET_CODE,
                         rv.status_code,
                         "Unable to submit a game score")
        self.assertEqual(loads(rv.data), True, "Unable to submit a game score")
        game_model = Game.query.get(game['game_id'])
        for bat in game_model.bats:
            self.bats_to_delete.append(bat)
        return [bat.json() for bat in game_model.bats]

    def submit_a_score_by_kik(self, kik, game, score, hr=[], ss=[]):
        """Submits a score & returns the list of bats created using kik api"""
        data = {'kik': kik,
                'game_id': game['game_id'],
                'score': score,
                'hr': hr,
                'ss': ss}
        rv = self.app.post(Routes['kiksubmitscore'],
                           data=data,
                           headers=KIK_HEADER)
        message = "Unable to submit a game score using kik api"
        self.assertEqual(SUCCESSFUL_GET_CODE, rv.status_code, message)
        self.assertEqual(loads(rv.data), True, message)
        game_model = Game.query.get(game['game_id'])
        for bat in game_model.bats:
            self.bats_to_delete.append(bat)
        return [bat.json() for bat in game_model.bats]

    def assertFunModelEqual(self, f1, f2, error_message=""):
        """Asserts the two fun json objects are equal"""
        self.assertEqual(f1['year'], f2['year'], error_message)
        self.assertEqual(f1['count'], f2['count'], error_message)

    def assertSponsorModelEqual(self, s1, s2, error_message=""):
        """Asserts the two sponsors json objects are equal"""
        self.assertEqual(s1['sponsor_id'], s2['sponsor_id'], error_message)
        self.assertEqual(s1['sponsor_name'], s2['sponsor_name'], error_message)
        self.assertEqual(s1['link'], s2['link'], error_message)
        self.assertEqual(s1['description'], s2['description'], error_message)
        self.assertEqual(s1['active'], s2['active'], error_message)

    def assertLeagueModelEqual(self, l1, l2, error_message=""):
        """Asserts the two league json objects are equal"""
        self.assertEqual(l1['league_name'], l2['league_name'], error_message)
        self.assertEqual(l1['league_id'], l2['league_id'], error_message)

    def assertGameModelEqual(self, g1, g2, error_message=""):
        """Asserts the two game json objects are equal"""
        self.assertEqual(g1['date'], g2['date'], error_message)
        self.assertEqual(g1['time'], g2['time'], error_message)
        self.assertEqual(g1['away_team_id'], g2['away_team_id'], error_message)
        self.assertEqual(g1['home_team_id'], g2['home_team_id'], error_message)
        self.assertEqual(g1['league_id'], g2['league_id'], error_message)
        self.assertEqual(g1['status'], g2['status'], error_message)
        self.assertEqual(g1['field'], g2['field'], error_message)
        self.assertEqual(g1['game_id'], g2['game_id'], error_message)

    def assertPlayerModelEqual(self, p1, p2, error_message=""):
        """Asserts the two player json objects are equal"""
        self.assertEqual(p1['player_id'], p2['player_id'], error_message)
        self.assertEqual(p1['player_name'], p2['player_name'], error_message)
        self.assertEqual(p1['gender'], p2['gender'], error_message)
        self.assertEqual(p1['active'], p2['active'], error_message)

    def assertTeamModelEqual(self, t1, t2, error_message=""):
        """Asserts the two team json objects are equal"""
        self.assertEqual(t1['team_id'], t2['team_id'], error_message)
        self.assertEqual(t1['color'], t2['color'], error_message)
        self.assertEqual(t1['sponsor_id'], t2['sponsor_id'], error_message)
        self.assertEqual(t1['league_id'], t2['league_id'], error_message)
        self.assertEqual(t1['year'], t2['year'], error_message)
        if (t1['captain'] is not None and t2['captain'] is not None):
            self.assertEqual(t1['captain']['player_id'],
                             t2['captain']['player_id'],
                             error_message)
        else:
            self.assertEqual(t1['captain'], t2['captain'], error_message)

    def assertEspysModelEqual(self, e1, e2, error_message=""):
        """Asserts the espys fun json objects are equal"""
        self.assertEqual(e1['team_id'], e2['team_id'], error_message)
        self.assertEqual(e1['sponsor_id'], e2['sponsor_id'], error_message)
        self.assertEqual(e1['description'], e2['description'], error_message)
        self.assertEqual(e1['points'], e2['points'], error_message)
        self.assertEqual(e1['receipt'], e2['receipt'], error_message)
        self.assertEqual(e1['time'], e2['time'], error_message)
        self.assertEqual(e1['date'], e2['date'], error_message)

    def assertBatModelEqual(self, b1, b2, error_message=""):
        """Asserts the two bat json objects are equal"""
        self.assertEqual(b1['bat_id'], b2['bat_id'], error_message)
        self.assertEqual(b1['team_id'], b2['team_id'], error_message)
        self.assertEqual(b1['game_id'], b2['game_id'], error_message)
        self.assertEqual(b1['rbi'], b2['rbi'], error_message)
        self.assertEqual(b1['inning'], b2['inning'], error_message)
        self.assertEqual(b1['player_id'], b2['player_id'], error_message)
        self.assertEqual(b1['hit'], b2['hit'], error_message)

    def postInvalidTest(self,
                        route,
                        params,
                        expected_status_code,
                        assert_function,
                        expect,
                        error_message=""):
        """Used to test an invalid post test"""
        rv = self.app.post(route, data=params, headers=headers)
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(expected_status_code, rv.status_code, error_message)
        assert_function(expect, loads(rv.data), error_message)

    def putTest(self,
                route,
                params,
                expected_status_code,
                assert_function,
                expected_object,
                error_message=""):
        """Used to test a put request"""
        rv = self.app.put(route, data=params, headers=headers)
        self.output(loads(rv.data))
        self.output(expected_object)
        self.assertEqual(expected_status_code, rv.status_code, error_message)
        assert_function(expected_object, loads(rv.data), error_message)

    def getTest(self,
                route,
                expected_status_code,
                assert_function,
                expected_object,
                error_message=""):
        """Used to test a get request"""
        rv = self.app.get(route, headers=headers)
        self.output(loads(rv.data))
        self.output(expected_object)
        assert_function(expected_object, loads(rv.data), error_message)
        self.assertEqual(expected_status_code, rv.status_code, error_message)

    def deleteValidTest(self,
                        route,
                        expected_status_code_after_deletion,
                        assert_function,
                        object_id,
                        expected_object,
                        expected_message,
                        error_message=""):
        """Used to test a delete request for a valid resource"""
        # check object exists
        self.getTest(route + "/" + str(object_id),
                     SUCCESSFUL_GET_CODE,
                     assert_function,
                     expected_object,
                     error_message=error_message)

        # delete object
        rv = self.app.delete(route + "/" + str(object_id), headers=headers)
        expect = None
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, error_message)
        self.assertEqual(rv.status_code, SUCCESSFUL_DELETE_CODE, error_message)

        # check object was deleted
        self.getTest(route + "/" + str(object_id),
                     expected_status_code_after_deletion,
                     self.assertEqual,
                     {"details": object_id, "message": expected_message},
                     error_message=error_message)

    def deleteInvalidTest(self,
                          route,
                          expected_status_code,
                          expected_message,
                          error_message=""):
        """Used to test a delete request for an invalid resource"""
        rv = self.app.delete(route + "/" + str(INVALID_ID),
                             headers=headers)
        expect = {'details': INVALID_ID, 'message': expected_message}
        self.output(loads(rv.data))
        self.output(expect)
        self.assertEqual(loads(rv.data), expect, error_message)
        self.assertEqual(rv.status_code, expected_status_code, error_message)

    def getListTest(self, route, error_message=""):
        """Runs a get test on lists"""
        done = False
        while not done:
            rv = self.app.get(route)
            self.assertEqual(rv.status_code,
                             SUCCESSFUL_GET_CODE,
                             error_message)
            pagination = loads(rv.data)
            if not pagination['has_next']:
                done = True
                self.assertTrue(len(pagination['items']) >= 0)
            else:
                self.assertTrue(pagination['next_url'] is not None,
                                error_message)
                self.assertTrue(len(pagination['items']) > 0)
                max_total = pagination['pages'] * PAGE_SIZE
                self.assertTrue(pagination['total'] <= max_total)
                route = pagination['next_url']


def addGame(tester, day="2014-02-10", time="22:40"):
    """Returns a created game (creates, league, sponsor, two teams)"""
    # add two teams, a sponsor and a league
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    home_team = tester.add_team("Black" + str(counter),
                                sponsor,
                                league,
                                VALID_YEAR)
    away_team = tester.add_team("White" + str(counter),
                                sponsor,
                                league,
                                VALID_YEAR)
    game = tester.add_game(day,
                           time,
                           home_team,
                           away_team,
                           league)
    return game


def addBat(tester, classification):
    """Returns a created bat

    (creates a league, sponsor, two teams, game, player)
    """
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    home_team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    away_team = tester.add_team("White", sponsor, league, VALID_YEAR)
    game = tester.add_game("2014-02-10",
                           "22:40",
                           home_team,
                           away_team,
                           league)
    player = tester.add_player("Test Player" + str(counter),
                               "TestPlayer" + str(counter) + "@mlsb.ca",
                               gender="M")
    bat = tester.add_bat(player, home_team, game, classification)
    return bat


def addEspy(tester, points):
    """Returns a espy transaction

    (Creates a league, sponsor, team and espys transaction)
    """
    counter = tester.get_counter()
    tester.increment_counter()
    league = tester.add_league("New League" + str(counter))
    sponsor = tester.add_sponsor("Sponsor" + str(counter))
    team = tester.add_team("Black", sponsor, league, VALID_YEAR)
    espy = tester.add_espys(team, sponsor, points=points)
    return espy
