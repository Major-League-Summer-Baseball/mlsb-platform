from api.model import \
    Player, Team, Bat, Sponsor, League, Game, Division, JoinLeagueRequest
from api.errors import \
    InvalidField, PlayerDoesNotExist, TeamDoesNotExist, LeagueDoesNotExist, \
    SponsorDoesNotExist, NonUniqueEmail, GameDoesNotExist, \
    DivisionDoesNotExist, HaveLeagueRequestException
from api.test.BaseTest import TestSetup, INVALID_ID, VALID_YEAR
from sqlalchemy.orm import undefer
from datetime import datetime
import unittest
import uuid


class SponsorModelTest(TestSetup):

    def testSponsorInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # valid data
            sponsor_name = str(uuid.uuid1())
            Sponsor(sponsor_name)
            Sponsor(
                sponsor_name,
                link="http://good-sponsor.ca",
                description="Good Descript"
            )
            # now bad stuff
            try:
                Sponsor(1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                Sponsor(sponsor_name, link=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                Sponsor(
                    sponsor_name,
                    link="http://good-sponsor.ca",
                    description=1
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testSponsorUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # valid sponsor
            sponsor_name = str(uuid.uuid1())
            new_sponsor_name = str(uuid.uuid1())
            s = Sponsor(sponsor_name)
            # valid update
            s.update(name=new_sponsor_name, link="New Link", description="new")
            # now bad stuff
            try:
                s.update(name=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                s.update(sponsor_name, link=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                s.update(
                    sponsor_name,
                    link="http://good-sponsor.ca",
                    description=1
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass


class PlayerModelTest(TestSetup):

    def testPlayerInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player_name = str(uuid.uuid1())
            email = player_name + "@mlsb.ca"
            Player(player_name, email)
            Player(
                player_name,
                email,
                gender="m",
                password="Good password"
            )
            # now bad stuff
            try:
                Player(1, email)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                Player(player_name, 1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                some_email = str(uuid.uuid1()) + "@mlsb.ca"
                self.add_player(str(uuid.uuid1()), some_email)
                Player(str(uuid.uuid1()), some_email)
                self.assertEqual(False, True, "Should raise email exception")
            except NonUniqueEmail:
                pass
            try:
                Player(player_name, email, gender="XX")
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testPlayerUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player_name = str(uuid.uuid1())
            email = player_name + "@mlsb.ca"
            new_player_name = str(uuid.uuid1())
            new_email = new_player_name + "@mlsb.ca"
            p1 = Player(player_name, email)
            p1.update(
                name=new_player_name,
                email=new_email,
                gender="f",
                password="n"
            )
            # now bad stuff
            try:
                p1.update(name=1, email=email)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                p1.update(name=player_name, email=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                some_email = str(uuid.uuid1()) + "@mlsb.ca"
                self.add_player(str(uuid.uuid1()), some_email)
                p1.update(name=str(uuid.uuid1()), email=some_email)
                self.assertEqual(False, True, "Should raise email exception")
            except NonUniqueEmail:
                pass
            try:
                p1.update(name=player_name, email=email, gender="XX")
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass


class LeagueModelTest(TestSetup):

    def testLeagueInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            League(str(uuid.uuid1()))
            # now bad stuff
            try:
                League(1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testLeagueUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = League(str(uuid.uuid1()))
            league.update(str(uuid.uuid1()))
            try:
                league.update(1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass


class DivisionModelTest(TestSetup):

    def testDivisionInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            Division(str(uuid.uuid1()))
            Division(str(uuid.uuid1()), shortname=str(uuid.uuid1()))
            # now invalid init
            try:
                Division(1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                Division(str(uuid.uuid1()), shortname=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testDivisionUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            division = Division(str(uuid.uuid1()))
            division.update(name=str(uuid.uuid1()))
            division.update(
                name=str(uuid.uuid1()),
                shortname=str(uuid.uuid1())
            )
            division.update(shortname=str(uuid.uuid1()))
            # now invalid updates
            try:
                division.update(name=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                division.update(shortname=1)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass


class TeamModelTest(TestSetup):

    def testTeamInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))

            # good Teams
            Team(
                color="Black",
                sponsor_id=sponsor['sponsor_id'],
                league_id=league['league_id']
            )
            Team(
                color="Green",
                sponsor_id=sponsor['sponsor_id'],
                league_id=league['league_id'],
                year=VALID_YEAR
            )

            # now for bad teams
            try:
                Team(
                    color="Black",
                    sponsor_id=INVALID_ID,
                    league_id=league['league_id']
                )
                self.assertEqual(False, True, "Should raise no sponsor")
            except SponsorDoesNotExist:
                pass
            try:
                Team(
                    color="Black",
                    sponsor_id=sponsor['sponsor_id'],
                    league_id=INVALID_ID
                )
                self.assertEqual(False, True, "Should raise no league")
            except LeagueDoesNotExist:
                pass
            try:
                Team(
                    color=1,
                    sponsor_id=sponsor['sponsor_id'],
                    league_id=league['league_id']
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                Team(
                    color="Black",
                    sponsor_id=sponsor['sponsor_id'],
                    league_id=league['league_id'],
                    year=1
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testTeamUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league_id = self.add_league(str(uuid.uuid1()))['league_id']
            sponsor_id = self.add_sponsor(str(uuid.uuid1()))['sponsor_id']

            # good Teams
            team = Team(
                color="Black", sponsor_id=sponsor_id, league_id=league_id
            )
            team.update(
                color="Green",
                sponsor_id=sponsor_id,
                league_id=league_id,
                year=VALID_YEAR
            )

            # now for bad teams
            try:
                team.update(
                    color="Black",
                    sponsor_id=INVALID_ID,
                    league_id=league_id
                )
                self.assertEqual(False, True, "Should raise no sponsor")
            except SponsorDoesNotExist:
                pass
            try:
                team.update(
                    color="Black",
                    sponsor_id=sponsor_id,
                    league_id=INVALID_ID
                )
                self.assertEqual(False, True, "Should raise no league")
            except LeagueDoesNotExist:
                pass
            try:
                team.update(
                    color=1,
                    sponsor_id=sponsor_id,
                    league_id=league_id
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                team.update(
                    color="Black",
                    sponsor_id=sponsor_id,
                    league_id=league_id,
                    year=1
                )
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testIsPlayerNotOnTeam(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Black", sponsor=sponsor, league=league
            )
            player = self.add_player(
                str(uuid.uuid1()),
                str(uuid.uuid1()) + "@mlsb.ca",
                gender="m"
            )
            team_model = Team.query.get(team['team_id'])
            player_model = Player.query.get(player['player_id'])
            self.assertFalse(
                team_model.is_player_on_team(player_model),
                "New player should not be on team"
            )

    def testIsPlayerOnTeam(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Black", sponsor=sponsor, league=league
            )
            player = self.add_player(
                str(uuid.uuid1()),
                str(uuid.uuid1()) + "@mlsb.ca",
                gender="m"
            )
            self.add_player_to_team(team, player)
            team_model = Team.query.get(team['team_id'])
            player_model = Player.query.get(player['player_id'])
            self.assertTrue(
                team_model.is_player_on_team(player_model),
                "New player added to team should be on team"
            )

    def testIsCaptainOnTeam(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Black", sponsor=sponsor, league=league
            )
            captain = self.add_player(
                str(uuid.uuid1()), str(uuid.uuid1()) + "@mlsb.ca", gender="m"
            )
            self.add_player_to_team(team, captain, captain=True)
            team_model = Team.query.get(team['team_id'])
            captain_model = Player.query.get(captain['player_id'])
            self.assertTrue(
                team_model.is_player_on_team(captain_model),
                "Captain of team should be on team"
            )

    def testIsNoneOnTeam(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Black", sponsor=sponsor, league=league
            )
            team_model = Team.query.get(team['team_id'])
            self.assertFalse(
                team_model.is_player_on_team(None),
                "None should not be on team"
            )

    def testInsertingPlayer(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Black",
                sponsor=sponsor,
                league=league
            )
            player = self.add_player(
                str(uuid.uuid1()),
                str(uuid.uuid1()) + "@mlsb.ca",
                gender="m"
            )
            team_model = Team.query.get(team['team_id'])
            team_model.insert_player(player['player_id'])
            self.assertTrue(
                team_model.is_player_on_team(
                    Player.query.get(player['player_id'])
                ),
                "Expecting player to be added to team"
            )

    def testRemovePlayer(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Blacl",
                sponsor=sponsor,
                league=league
            )
            player = self.add_player(
                str(uuid.uuid1()),
                str(uuid.uuid1()) + "@mlsb.ca",
                gender="m"
            )
            self.add_player_to_team(team, player, captain=True)
            team_model = Team.query.get(team['team_id'])
            team_model.remove_player(player['player_id'])
            self.assertFalse(
                team_model.is_player_on_team(
                    Player.query.get(player['player_id'])
                ),
                "Expecting player to be removed from team"
            )

    def testEspsysTotal(self):
        """Test that espys total work"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team = self.add_team(
                color="Blacl",
                sponsor=sponsor,
                league=league
            )

            # award the team 3 espys points in from two different
            # transactions
            espy_one = self.add_espys(team, sponsor, points=1)
            espy_two = self.add_espys(team, sponsor, points=2)

            # assert that their total is 3 points
            self.assertEqual(
                Team.query.options(
                    undefer('espys_total')).get(team['team_id']).espys_total,
                espy_one['points'] + espy_two['points'],
                "Expecting 3 espys points to be awarded"
            )


class GameModelTest(TestSetup):

    def testGameInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            league = self.add_league(str(uuid.uuid1()))
            league_id = league['league_id']
            division = self.add_division(str(uuid.uuid1()))
            division_id = division['division_id']
            home_team_id = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )['team_id']
            away_team_id = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )['team_id']
            # good game
            Game(
                getDateString(),
                getTimeString(),
                home_team_id,
                away_team_id,
                league_id,
                division_id
            )
            try:
                Game(
                    "x",
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    division_id
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    division_id,
                    status=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    division_id,
                    field=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    INVALID_ID,
                    away_team_id,
                    league_id, division_id
                )
                self.assertEqual(True, False, "should raise no team")
            except TeamDoesNotExist:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    INVALID_ID,
                    league_id,
                    division_id
                )
                self.assertEqual(True, False, "should raise no team")
            except TeamDoesNotExist:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    INVALID_ID,
                    division_id
                )
                self.assertEqual(True, False, "should raise no league")
            except LeagueDoesNotExist:
                pass
            try:
                Game(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    INVALID_ID
                )
                self.assertEqual(True, False, "should raise no league")
            except DivisionDoesNotExist:
                pass

    def testGameUpdate(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            league = self.add_league(str(uuid.uuid1()))
            league_id = league['league_id']
            division = self.add_division(str(uuid.uuid1()))
            division_id = division['division_id']
            home_team_id = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )['team_id']
            away_team_id = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )['team_id']
            # good game
            g = Game(
                getDateString(),
                getTimeString(),
                home_team_id,
                away_team_id,
                league_id,
                division_id
            )
            try:
                g.update(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    status=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                g.update(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    league_id,
                    field=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                g.update(
                    getDateString(),
                    getTimeString(),
                    INVALID_ID,
                    away_team_id,
                    league_id
                )
                self.assertEqual(True, False, "should raise no team")
            except TeamDoesNotExist:
                pass
            try:
                g.update(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    INVALID_ID,
                    league_id
                )
                self.assertEqual(True, False, "should raise no team")
            except TeamDoesNotExist:
                pass
            try:
                g.update(
                    getDateString(),
                    getTimeString(),
                    home_team_id,
                    away_team_id,
                    INVALID_ID
                )
                self.assertEqual(True, False, "should raise no league")
            except LeagueDoesNotExist:
                pass


class JoinLeagueRequestTest(TestSetup):
    """Test the join league request model"""

    def testJoinLeagueRequestInit(self):
        """ Test the constructor validates the given data"""
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player = str(uuid.uuid1())
            email = player + "@mlsb.ca"
            some_gender = "m"
            color = str(uuid.uuid1())
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            no_team = Team(
                color="Black",
                sponsor_id=sponsor['sponsor_id'],
                league_id=league['league_id']
            )
            team_json = self.add_team(color, sponsor=sponsor, league=league)
            team = Team.query.get(team_json['team_id'])

            # good request and test json method
            league_request = JoinLeagueRequest(email, player, team, some_gender)
            league_request.json()

            # bad stuff
            try:
                JoinLeagueRequest(1, player, team, some_gender)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                JoinLeagueRequest(email, 1, team, some_gender)
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass
            try:
                JoinLeagueRequest(email, player, "wrong team", some_gender)
                self.assertEqual(
                    False, True, "Should raise team does not exist"
                )
            except TeamDoesNotExist:
                pass
            try:
                JoinLeagueRequest(email, player, no_team, some_gender)
                self.assertEqual(
                    False, True, "Should raise team does not exist"
                )
            except TeamDoesNotExist:
                pass
            try:
                JoinLeagueRequest(email, player, team, "XX")
                self.assertEqual(False, True, "Should raise invalid field")
            except InvalidField:
                pass

    def testAcceptJoinLeagueRequestNewPlayer(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player = str(uuid.uuid1())
            email = player + "@mlsb.ca"
            some_gender = "m"
            color = str(uuid.uuid1())
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team_json = self.add_team(color, sponsor=sponsor, league=league)
            team = Team.query.get(team_json['team_id'])
            league_request = JoinLeagueRequest(email, player, team, some_gender)
            accepted_player = league_request.accept_request()

            # check player is one team now
            self.assertTrue(
                accepted_player.id is not None,
                "Create player account when joining team"
            )
            team = Team.query.get(team_json['team_id'])
            self.assertTrue(
                bool([
                    True for p in team.players
                    if p.email == email and p.id is not None
                ]),
                "New player added was not added to team"
            )

    def testAcceptJoinLeagueRequestExistingPlayer(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            name = str(uuid.uuid1())
            email = name + "@mlsb.ca"
            some_gender = "m"
            player = self.add_player(name, email, gender=some_gender)
            color = str(uuid.uuid1())
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team_json = self.add_team(color, sponsor=sponsor, league=league)
            team = Team.query.get(team_json['team_id'])
            league_request = JoinLeagueRequest(email, player, team, some_gender)
            accepted_player = league_request.accept_request()

            # check player is one team now
            self.assertEqual(
                accepted_player.id, player['player_id'],
                "Use player account when joining team"
            )
            team = Team.query.get(team_json['team_id'])
            self.assertTrue(
                bool([
                    True for p in team.players
                    if p.id == player['player_id']
                ]),
                "Existing player added was not added to team"
            )

    def testAcceptJoinLeagueRequestTwice(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            name = str(uuid.uuid1())
            email = name + "@mlsb.ca"
            some_gender = "m"
            player = self.add_player(name, email, gender=some_gender)
            color = str(uuid.uuid1())
            league = self.add_league(str(uuid.uuid1()))
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            team_json = self.add_team(color, sponsor=sponsor, league=league)
            team = Team.query.get(team_json['team_id'])
            league_request = JoinLeagueRequest(email, player, team, some_gender)
            league_request.accept_request()
            try:
                league_request.accept_request()
                self.assertTrue(
                    False, "Should not be able to accept request league twice")
            except HaveLeagueRequestException:
                pass


class BatModelTest(TestSetup):

    def testBatInit(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player_name = str(uuid.uuid1())
            email = player_name + "@mlsb.ca"
            player = self.add_player(player_name, email)
            player_id = player['player_id']
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            league = self.add_league(str(uuid.uuid1()))
            division = self.add_division(str(uuid.uuid1()))
            home_team = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )
            home_team_id = home_team['team_id']
            away_team = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )
            game = self.add_game(
                getDateString(),
                getTimeString(),
                home_team,
                away_team,
                league,
                division
            )
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
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            player_name = str(uuid.uuid1())
            email = player_name + "@mlsb.ca"
            player = self.add_player(player_name, email)
            player_id = player['player_id']
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            league = self.add_league(str(uuid.uuid1()))
            division = self.add_division(str(uuid.uuid1()))
            home_team = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )
            home_team_id = home_team['team_id']
            away_team = self.add_team(
                str(uuid.uuid1()), sponsor, league, VALID_YEAR
            )
            game = self.add_game(
                getDateString(),
                getTimeString(),
                home_team,
                away_team,
                league,
                division
            )
            game_id = game['game_id']
            # good bat
            b = Bat(player_id, home_team_id, game_id, "s", inning=1, rbi=1)
            # now for the bad stuff
            try:
                b.update(
                    player_id=player_id,
                    team_id=home_team_id,
                    game_id=game_id,
                    hit="XX",
                    inning=1,
                    rbi=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                b.update(
                    player_id=player_id,
                    team_id=home_team_id,
                    game_id=game_id,
                    hit="s",
                    inning=-1,
                    rbi=1
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                b.update(
                    player_id=player_id,
                    team_id=home_team_id,
                    game_id=game_id,
                    hit="s",
                    inning=1,
                    rbi=1000
                )
                self.assertEqual(True, False, "should raise invalid field")
            except InvalidField:
                pass
            try:
                b.update(
                    player_id=INVALID_ID,
                    team_id=home_team_id,
                    game_id=game_id,
                    hit="s",
                    inning=1,
                    rbi=1
                )
                self.assertEqual(True, False, "should raise no player")
            except PlayerDoesNotExist:
                pass
            try:
                b.update(
                    player_id=player_id,
                    team_id=INVALID_ID,
                    game_id=game_id,
                    hit="s",
                    inning=1,
                    rbi=1
                )
                self.assertEqual(True, False, "should raise no team")
            except TeamDoesNotExist:
                pass
            try:
                b.update(
                    player_id=player_id,
                    team_id=home_team_id,
                    game_id=INVALID_ID,
                    hit="s",
                    inning=1,
                    rbi=1
                )
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
