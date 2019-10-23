'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: Holds the tests for the model
'''
from api.model import Player, Team, Bat, Sponsor, League, Game
from api.errors import InvalidField, PlayerDoesNotExist, TeamDoesNotExist,\
    LeagueDoesNotExist, SponsorDoesNotExist,\
    NonUniqueEmail, GameDoesNotExist
from api.test.BaseTest import TestSetup, INVALID_ID, VALID_YEAR
from datetime import datetime
import unittest
import uuid


class SponsorModelTest(TestSetup):

    def testSponsorInit(self):
        # valid data
        Sponsor("Good Sponsor")
        Sponsor("Good Sponsor",
                link="http://good-sponsor.ca",
                description="Good Descript")
        # now bad stuff
        try:
            Sponsor(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            Sponsor("Good Sponsor",
                    link=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            Sponsor("Good Sponsor",
                    link="http://good-sponsor.ca",
                    description=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testSponsorUpdate(self):
        # valid sponsor
        s = Sponsor("Good Sponsor")
        # valid update
        s.update(name="New Sponsor", link="New Link", description="new")
        # now bad stuff
        try:
            s.update(name=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            s.update("Good Sponsor",
                     link=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            s.update("Good Sponsor",
                     link="http://good-sponsor.ca",
                     description=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass


class PlayerModelTest(TestSetup):

    def testPlayerInit(self):
        Player("Good Player", "good@mlsb.ca")
        Player("Good Player",
               "good@mlsb.ca",
               gender="m",
               password="Good password")
        # now bad stuff
        try:
            Player(1, "good@mlsb.ca")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            Player("Good Player", 1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            self.add_player("first player", "fras2560@mlsb.ca")
            Player("second player", "fras2560@mlsb.ca")
            self.assertEqual(False, True, "Should raise email exception")
        except NonUniqueEmail:
            pass
        try:
            Player("Good Player", "good@mlsb.ca", gender="XX")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testPlayerUpdate(self):
        p1 = Player("Good Player", "good@mlsb.ca")
        p1.update(name="new name",
                  email="new@mlsb.ca",
                  gender="f",
                  password="n")
        # now bad stuff
        try:
            p1.update(name=1, email="good@mlsb.ca")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            p1.update(name="Good Player", email=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            self.add_player("first player", "fras2560@mlsb.ca")
            p1.update(name="second player", email="fras2560@mlsb.ca")
            self.assertEqual(False, True, "Should raise email exception")
        except NonUniqueEmail:
            pass
        try:
            p1.update(name="Good Player", email="good@mlsb.ca", gender="XX")
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass


class LeagueModelTest(TestSetup):

    def testLeagueInit(self):
        League("Monday & Wednesday")
        # now bad stuff
        try:
            League(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testLeagueUpdate(self):
        league = League("Monday & Wednesday")
        league.update("Tuesday & Thursday")
        try:
            league.update(1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass


class TeamModelTest(TestSetup):

    def testTeamInit(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")

        # good Teams
        Team(color="Black",
             sponsor_id=sponsor['sponsor_id'],
             league_id=league['league_id'])
        Team(color="Green",
             sponsor_id=sponsor['sponsor_id'],
             league_id=league['league_id'],
             year=VALID_YEAR)

        # now for bad teams
        try:
            Team(color="Black",
                 sponsor_id=INVALID_ID,
                 league_id=league['league_id'])
            self.assertEqual(False, True, "Should raise no sponsor")
        except SponsorDoesNotExist:
            pass
        try:
            Team(color="Black",
                 sponsor_id=sponsor['sponsor_id'],
                 league_id=INVALID_ID)
            self.assertEqual(False, True, "Should raise no league")
        except LeagueDoesNotExist:
            pass
        try:
            Team(color=1,
                 sponsor_id=sponsor['sponsor_id'],
                 league_id=league['league_id'])
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            Team(color="Black",
                 sponsor_id=sponsor['sponsor_id'],
                 league_id=league['league_id'],
                 year=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testTeamUpdate(self):
        league_id = self.add_league("TestModelLeague")['league_id']
        sponsor_id = self.add_sponsor("TestModelSponsor")['sponsor_id']

        # good Teams
        team = Team(color="Black",
                    sponsor_id=sponsor_id,
                    league_id=league_id)
        team.update(color="Green",
                    sponsor_id=sponsor_id,
                    league_id=league_id,
                    year=VALID_YEAR)

        # now for bad teams
        try:
            team.update(color="Black",
                        sponsor_id=INVALID_ID,
                        league_id=league_id)
            self.assertEqual(False, True, "Should raise no sponsor")
        except SponsorDoesNotExist:
            pass
        try:
            team.update(color="Black",
                        sponsor_id=sponsor_id,
                        league_id=INVALID_ID)
            self.assertEqual(False, True, "Should raise no league")
        except LeagueDoesNotExist:
            pass
        try:
            team.update(color=1,
                        sponsor_id=sponsor_id,
                        league_id=league_id)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass
        try:
            team.update(color="Black",
                        sponsor_id=sponsor_id,
                        league_id=league_id,
                        year=1)
            self.assertEqual(False, True, "Should raise invalid field")
        except InvalidField:
            pass

    def testIsPlayerNotOnTeam(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        player = self.add_player(
            str(uuid.uuid1()), str(uuid.uuid1()) + "@mlsb.ca", gender="m")
        team_model = Team.query.get(team['team_id'])
        player_model = Player.query.get(player['player_id'])
        self.assertFalse(team_model.is_player_on_team(
            player_model), "New player should not be on team")

    def testIsPlayerOnTeam(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        player = self.add_player(
            str(uuid.uuid1()), str(uuid.uuid1()) + "@mlsb.ca", gender="m")
        self.add_player_to_team(team, player)
        team_model = Team.query.get(team['team_id'])
        player_model = Player.query.get(player['player_id'])
        self.assertTrue(team_model.is_player_on_team(
            player_model), "New player added to team should be on team")

    def testIsCaptainOnTeam(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        captain = self.add_player(
            str(uuid.uuid1()), str(uuid.uuid1()) + "@mlsb.ca", gender="m")
        self.add_player_to_team(team, captain, captain=True)
        team_model = Team.query.get(team['team_id'])
        captain_model = Player.query.get(captain['player_id'])
        self.assertTrue(team_model.is_player_on_team(
            captain_model), "Captain of team should be on team")

    def testIsNoneOnTeam(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        team_model = Team.query.get(team['team_id'])
        self.assertFalse(team_model.is_player_on_team(
            None), "None should not be on team")

    def testInsertingPlayer(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        player = self.add_player(str(uuid.uuid1()), str(
            uuid.uuid1()) + "@mlsb.ca", gender="m")
        team_model = Team.query.get(team['team_id'])
        team_model.insert_player(player['player_id'])
        self.assertTrue(team_model.is_player_on_team(Player.query.get(
            player['player_id'])), "Expecting player to be added to team")

    def testRemovePlayer(self):
        league = self.add_league("TestModelLeague")
        sponsor = self.add_sponsor("TestModelSponsor")
        team = self.add_team(color="Blacl",
                             sponsor=sponsor,
                             league=league)
        player = self.add_player(str(uuid.uuid1()), str(
            uuid.uuid1()) + "@mlsb.ca", gender="m")
        self.add_player_to_team(team, player, captain=True)
        team_model = Team.query.get(team['team_id'])
        team_model.remove_player(player['player_id'])
        self.assertFalse(team_model.is_player_on_team(Player.query.get(
            player['player_id'])), "Expecting player to be removed from team")


class GameModelTest(TestSetup):

    def testGameInit(self):
        sponsor = self.add_sponsor("TestModelSponsor")
        league = self.add_league("TestModelLeague")
        league_id = league['league_id']
        home_team_id = self.add_team("TestModelHomeTeam",
                                     sponsor,
                                     league,
                                     VALID_YEAR)['team_id']
        away_team_id = self.add_team("TestModelAwayTeam",
                                     sponsor,
                                     league,
                                     VALID_YEAR)['team_id']
        # good game
        Game(getDateString(), getTimeString(),
             home_team_id, away_team_id, league_id)
        try:
            Game("x", getTimeString(), home_team_id, away_team_id, league_id)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Game(getDateString(),
                 getTimeString(),
                 home_team_id,
                 away_team_id,
                 league_id,
                 status=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Game(getDateString(),
                 getTimeString(),
                 home_team_id,
                 away_team_id,
                 league_id,
                 field=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Game(getDateString(), getTimeString(),
                 INVALID_ID, away_team_id, league_id)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            Game(getDateString(), getTimeString(),
                 home_team_id, INVALID_ID, league_id)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            Game(getDateString(),
                 getTimeString(), home_team_id, away_team_id, INVALID_ID)
            self.assertEqual(True, False, "should raise no league")
        except LeagueDoesNotExist:
            pass

    def testGameUpdate(self):
        sponsor = self.add_sponsor("TestModelSponsor")
        league = self.add_league("TestModelLeague")
        league_id = league['league_id']
        home_team_id = self.add_team("TestModelHomeTeam",
                                     sponsor,
                                     league,
                                     VALID_YEAR)['team_id']
        away_team_id = self.add_team("TestModelAwayTeam",
                                     sponsor,
                                     league,
                                     VALID_YEAR)['team_id']
        # good game
        g = Game(getDateString(),
                 getTimeString(), home_team_id, away_team_id, league_id)
        try:
            g.update(getDateString(),
                     getTimeString(),
                     home_team_id,
                     away_team_id,
                     league_id,
                     status=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            g.update(getDateString(),
                     getTimeString(),
                     home_team_id,
                     away_team_id,
                     league_id,
                     field=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            g.update(getDateString(),
                     getTimeString(),
                     INVALID_ID,
                     away_team_id,
                     league_id)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            g.update(getDateString(),
                     getTimeString(),
                     home_team_id,
                     INVALID_ID,
                     league_id)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            g.update(getDateString(),
                     getTimeString(),
                     home_team_id,
                     away_team_id,
                     INVALID_ID)
            self.assertEqual(True, False, "should raise no league")
        except LeagueDoesNotExist:
            pass


class BatModelTest(TestSetup):

    def testBatInit(self):
        player = self.add_player("ModelTestPlayer", "ModelTestPlayer@mlsb.ca")
        player_id = player['player_id']
        sponsor = self.add_sponsor("TestModelSponsor")
        league = self.add_league("TestModelLeague")
        home_team = self.add_team("TestModelHomeTeam",
                                  sponsor,
                                  league,
                                  VALID_YEAR)
        home_team_id = home_team['team_id']
        away_team = self.add_team("TestModelAwayTeam",
                                  sponsor,
                                  league,
                                  VALID_YEAR)
        game = self.add_game(getDateString(),
                             getTimeString(), home_team, away_team, league)
        game_id = game['game_id']

        # good bat
        Bat(player_id, home_team_id, game_id, "s", inning=1, rbi=1)

        # now for the bad stuff
        try:
            Bat(player_id, home_team_id, game_id, "XX", inning=1, rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Bat(player_id, home_team_id, game_id, "s", inning=-1, rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Bat(player_id, home_team_id, game_id, "s", inning=1, rbi=1000)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            Bat(INVALID_ID, home_team_id, game_id, "s", inning=1, rbi=1)
            self.assertEqual(True, False, "should raise no player")
        except PlayerDoesNotExist:
            pass
        try:
            Bat(player_id, INVALID_ID, game_id, "s", inning=1, rbi=1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            Bat(player_id, home_team_id, INVALID_ID, "s", inning=1, rbi=1)
            self.assertEqual(True, False, "should raise no league")
        except GameDoesNotExist:
            pass

    def testBatUpdate(self):
        player = self.add_player("ModelTestPlayer", "ModelTestPlayer@mlsb.ca")
        player_id = player['player_id']
        sponsor = self.add_sponsor("TestModelSponsor")
        league = self.add_league("TestModelLeague")
        home_team = self.add_team("TestModelHomeTeam",
                                  sponsor,
                                  league,
                                  VALID_YEAR)
        home_team_id = home_team['team_id']
        away_team = self.add_team("TestModelAwayTeam",
                                  sponsor,
                                  league,
                                  VALID_YEAR)
        game = self.add_game(getDateString(),
                             getTimeString(), home_team, away_team, league)
        game_id = game['game_id']
        # good bat
        b = Bat(player_id, home_team_id, game_id, "s", inning=1, rbi=1)
        # now for the bad stuff
        try:
            b.update(player_id=player_id,
                     team_id=home_team_id,
                     game_id=game_id,
                     hit="XX",
                     inning=1,
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=player_id,
                     team_id=home_team_id,
                     game_id=game_id,
                     hit="s",
                     inning=-1,
                     rbi=1)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=player_id,
                     team_id=home_team_id,
                     game_id=game_id,
                     hit="s",
                     inning=1,
                     rbi=1000)
            self.assertEqual(True, False, "should raise invalid field")
        except InvalidField:
            pass
        try:
            b.update(player_id=INVALID_ID,
                     team_id=home_team_id,
                     game_id=game_id,
                     hit="s",
                     inning=1,
                     rbi=1)
            self.assertEqual(True, False, "should raise no player")
        except PlayerDoesNotExist:
            pass
        try:
            b.update(player_id=player_id,
                     team_id=INVALID_ID,
                     game_id=game_id,
                     hit="s",
                     inning=1,
                     rbi=1)
            self.assertEqual(True, False, "should raise no team")
        except TeamDoesNotExist:
            pass
        try:
            b.update(player_id=player_id,
                     team_id=home_team_id,
                     game_id=INVALID_ID,
                     hit="s",
                     inning=1,
                     rbi=1)
            self.assertEqual(True, False, "should raise no league")
        except GameDoesNotExist:
            pass


def getDateString():
    """Returns the current date string"""
    return datetime.now().strftime("%Y-%m-%d")


def getTimeString():
    """Returns the current time string"""
    return datetime.now().strftime("%H:%M")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
