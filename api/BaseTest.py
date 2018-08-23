'''
Created on Apr 12, 2016

@author: Dallas
'''
from api import app
from api import DB
from pprint import PrettyPrinter
from api.model import Player, Team, Sponsor, League, Game, Bat, Espys, Fun
from datetime import datetime, timedelta
from base64 import b64encode
from datetime import date
import unittest
import tempfile
import os


# environment variables
ADMIN = os.environ['ADMIN']
PASSWORD = os.environ['PASSWORD']
KIK = os.environ['KIK']
KIKPW = os.environ['KIKPW']

headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' + PASSWORD, "utf-8")).decode("ascii")
}

kik = {
    'Authorization': 'Basic %s' % b64encode(bytes(KIK + ':' + KIKPW, "utf-8")).decode("ascii")
}


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.show_results = False
        self.pp = PrettyPrinter(indent=4)
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.d = "2014-8-23"
        self.t = "11:37"
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.toDelete = []
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
        for item in reversed(self.toDelete):
            try:
                DB.session.delete(item)
                DB.session.commit()
            except:
                pass

    def tables_created(self):
        # TODO figure out how to check if tables are created
        return True

    def output(self, data):
        if self.show_results:
            self.pp.pprint(data)

    def addFun(self, count, year=date.today().year):
        fun = Fun(year=year, count=count)
        self.toDelete.append(fun)
        DB.session.add(fun)
        DB.session.commit()
        return fun.json()

    def addSponsor(self, sponsor_name, link=None, description=None, active=True, nickname=None):
        sponsor = Sponsor(sponsor_name, link=link, description=description, active=active, nickname=nickname)
        self.toDelete.append(sponsor)
        DB.sesion.add(sponsor)
        DB.session.commit()
        return sponsor.json()

    def addLeague(self, league_name):
        league = League(name=league_name)
        self.toDelete.append(league)
        DB.sesion.add(sponsor)
        DB.session.commit()
        return league.json()

    def addTeam(self, color, sponsor=None, league=None, year=date.today().year):
        team = Team(color=color, sponsor_id=sponsor.id, league_id=league.id, year=year)
        self.toDelete.append(team)
        DB.session.add(team)
        DB.session.commit()
        return team.json()

    def addGame(self, date, time, home_team, away_team, league, status="", field=""):
        game = Game(date, time, home_team.id, away_team.id, league.id, status=status, field=field)
        self.toDelete(game)
        DB.session.add(game)
        DB.session.commit()
        return game.json()

    def addBat(self, player, team, game, classification, inning=1, rbi=0):
        bat = Bat(player.id, team.id, game.id, classification, inning=inning, rbi=rbi)
        self.toDelete.append(bat)
        DB.session.add(bat)
        DB.session.commit()
        return bat.json()

    def addEspys(self, team, sponsor, description=None, points=0.0, receipt=None, time=None, date=None):
        espy = Espys(team.id, sponsor_id=sponsor.id, description=description, points=points, receipt=receipt, time=time, date=date)
        self.toDelete.append(espy)
        DB.session.add(espy)
        DB.session.commit()
        return espy.json()

    def assertFunModelEqual(self, f1, f2, error_message=""):
        """Asserts the two fun json objects are equal"""
        self.assertEqual(f1['year'], f2['year'], error_message,)
        self.assertEqual(f1['count'], f2['count'], error_message,)

    def assertLeagueModelEqual(self, l1, l2, error_message=""):
        """Asserts the two league json objects are equal"""
        self.assertEqual(l1['name'], l2['name'], error_message,)
        self.assertEqual(l1['league_id'], l2['league_id'], error_message,)

    def assertGameModelEqual(self, g1, g2, error_message=""):
        """Asserts the two game json objects are equal"""
        self.assertEqual(g1['date'], g2['date'], error_message,)
        self.assertEqual(g1['time'], g2['time'], error_message,)
        self.assertEqual(g1['away_team_id'], g2['away_team_id'], error_message,)
        self.assertEqual(g1['home_team_id'], g2['home_team_id'], error_message,)
        self.assertEqual(g1['league_id'], g2['league_id'], error_message,)
        self.assertEqual(g1['status'], g2['status'], error_message,)
        self.assertEqual(g1['field'], g2['field'], error_message,)
        self.assertEqual(g1['game_id'], g2['game_id'], error_message,)

    def assertPlayerModelEqual(self, p1, p2, error_message=""):
        """Asserts the two player json objects are equal"""
        self.assertEqual(p1['player_id'], p2['player_id'], error_message,)
        self.assertEqual(p1['name'], p2['name'], error_message,)
        self.assertEqual(p1['gender'], p2['gender'], error_message,)
        self.assertEqual(p1['active'], p2['active'], error_message,)

    def assertTeamModelEqual(self, t1, t2, error_message=""):
        """Asserts the two team json objects are equal"""
        self.assertEqual(t1['team_id'], t2['team_id'], error_meessage)
        self.assertEqual(t1['color'], t2['color'], error_meessage)
        self.assertEqual(t1['sponsor_id'], t2['sponsor_id'], error_meessage)
        self.assertEqual(t1['league_id'], t2['league_id'], error_meessage)
        self.assertEqual(t1['year'], t2['year'], error_meessage)
        if (t1['captain'] != None and t2['captain'] != None):
            self.assertEqual(t1['captain']['player_id'],
                             t2['captain']['player_id'],
                             error_meessage)
        else:
            self.assertEqual(t1.player_id, t2['captain'], error_meessage)

    def assertEspysModelEqual(self, e1, e2, error_message=""):
        """Asserts the espys fun json objects are equal"""
        self.assertEqual(e1['team_id'], e2['team_id'], error_message,)
        self.assertEqual(e1['sponsor_id'], e2['sponsor_id'], error_message,)
        self.assertEqual(e1['description'], e2['description'], error_message,)
        self.assertEqual(e1['points'], e2['points'], error_message,)
        self.assertEqual(e1['receipt'], e2['recipt'], error_message,)
        self.assertEqual(e1['time'], e2['time'], error_message,)
        self.assertEqual(e1['date'], e2['date'], error_message,)

    def assertBatModelEqual(self, b1, b2, error_message=""):
        """Asserts the two bat json objects are equal"""
        self.assertEqual(b1['bat_id'], b2['bat_id'], error_message)
        self.assertEqual(b1['team_id'], b2['team_id'], error_message)
        self.assertEqual(b1['game_id'], b2['game_id'], error_message)
        self.assertEqual(b1['rbi'], b2['rbi'], error_message)
        self.assertEqual(b1['inning'], b2['inning'], error_message)
        self.assertEqual(b1['player_id'], b2['player_id'], error_message)
        self.assertEqual(b1['hit'], b2['hit'], error_message)



