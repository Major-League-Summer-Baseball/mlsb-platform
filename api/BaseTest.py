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
        return fun

    def addSponsor(self, sponsor_name, link=None, description=None, active=True, nickname=None):
        sponsor = Sponsor(sponsor_name, link=link, description=description, active=active, nickname=nickname)
        self.toDelete.append(sponsor)
        DB.sesion.add(sponsor)
        DB.session.commit()
        return sponsor

    def addLeague(self, league_name):
        league = League(name=league_name)
        self.toDelete.append(league)
        DB.sesion.add(sponsor)
        DB.session.commit()
        return league

    def addTeam(color, sponsor=None, league=None, year=date.today().year):
        team = Team(color=color, sponsor_id=sponsor.id, league_id=league.id, year=year)
        self.toDelete.append(team)
        DB.session.add(team)
        DB.session.commit()
        return team

    def addGame(date, time, home_team, away_team, league, status="", field=""):
        game = Game(date, time, home_team.id, away_team.id, league.id, status=status, field=field)
        self.toDelete(game)
        DB.session.add(game)
        DB.session.commit()
        return game

    def addBat(player, team, game, classification, inning=1, rbi=0):
        bat = Bat(player.id, team.id, game.id, classification, inning=inning, rbi=rbi)
        self.toDelete.append(bat)
        DB.session.add(bat)
        DB.session.commit()
        return bat

    def addEspys(team, sponsor, description=None, points=0.0, receipt=None, time=None, date=None):
        espy = Espys(team.id, sponsor_id=sponsor.id, description=description, points=points, receipt=receipt, time=time, date=date)
        self.toDelete.append(espy)
        DB.session.add(espy)
        DB.session.commit()
        return espy
