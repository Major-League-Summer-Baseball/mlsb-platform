'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests all the advanced fun APIs
'''
from api.routes import Routes
from api.test.BaseTest import TestSetup, SUCCESSFUL_GET_CODE, INVALID_ID
from datetime import datetime
import uuid


class TestFun(TestSetup):

    def testStaticFileNotYearSpecific(self):
        # pages that do not need a year
        self.assertSuccessfulRoute(Routes['logo'],
                                   "Logo page should give a 200")
        self.assertSuccessfulRoute(Routes['privacy'],
                                   "Privacy page should give a 200")

    def testSponsorsPages(self):
        sponsor_name = str(uuid.uuid1())
        sponsor = self.add_sponsor(sponsor_name)

        # get the sponsor picture using sponsor name or id
        route = Routes['sponsorspicture'] + "/{}".format(sponsor_name)
        self.assertSuccessfulRoute(route, "Get sponsor picture from name")
        route = Routes['sponsorspicture'] + "/{}".format(sponsor['sponsor_id'])
        self.assertSuccessfulRoute(route, "Get sponsor picture from id")

        # get the sponsor page for all sponsors for a specific sponsor
        current_year = current_year = datetime.now().year
        route = Routes['sponsorspage'] + "/{}".format(current_year)
        self.assertSuccessfulRoute(route, "Get a page of all the sponsors")
        route = Routes['sponsorspage'] + "/{}/{}".format(current_year,
                                                         sponsor['sponsor_id'])
        self.assertSuccessfulRoute(route, "Get a page of specific sponsor")

        # get a non-existent sponsor
        route = Routes['sponsorspicture'] + "/{}".format(str(uuid.uuid1()))
        self.assertSuccessfulRoute(route, "Get non-existent sponsor picture")
        route = Routes['sponsorspicture'] + "/{}".format(INVALID_ID)
        self.assertSuccessfulRoute(route, "Get sponsor picture from id")
        route = Routes['sponsorspage'] + "/{}/{}".format(current_year,
                                                         INVALID_ID)
        self.assertSuccessfulRoute(route, "Get a page of non-existent sponsor")

    def testTeamPages(self):
        current_year = datetime.now().year

        # test team with a sponsor
        sponsor = self.add_sponsor(str(uuid.uuid1()))
        league = self.add_league(str(uuid.uuid1()))
        team_with_sponsor = self.add_team(
            "white", sponsor=sponsor, league=league)
        route = (Routes['teampicture'] +
                 "/{}".format(team_with_sponsor['team_id']))
        self.assertSuccessfulRoute(route,
                                   "Get picture of team with a sponsor")
        route = (Routes['teampage'] +
                 "/{}/{}".format(current_year, team_with_sponsor['team_id']))
        self.assertSuccessfulRoute(route,
                                   "Get page of team with a sponsor")

        # test non-existent team
        route = Routes['teampicture'] + "/{}".format(INVALID_ID)
        self.assertSuccessfulRoute(route,
                                   "Get picture of non-existent team")
        route = Routes['teampage'] + "/{}/{}".format(current_year, INVALID_ID)
        self.assertSuccessfulRoute(route,
                                   "Get page of non-existent team")

    def testPlayerPage(self):
        current_year = datetime.now().year

        # test player
        player_name = str(uuid.uuid1())
        player = self.add_player(
            player_name, player_name + "@mlsb.ca", gender="F")
        route = Routes['playerpage'] +\
            "/{}/{}".format(current_year, player['player_id'])
        self.assertSuccessfulRoute(route, 'Get page of a player')

        # test non-existent player
        route = Routes['playerpage'] +\
            "/{}/{}".format(current_year, INVALID_ID)
        self.assertSuccessfulRoute(route, 'Get page of a non-existent player')

    def testPostPages(self):
        year_with_posts = 2016
        # get all the posts
        route = Routes['posts'] + "/{}".format(year_with_posts)
        self.assertSuccessfulRoute(route, " Get all the posts descriptions")
        # get a sinle post plain or json
        plain_route = (Routes['posts'] + "/{}/{}/{}/plain"
                       .format(year_with_posts, "20160422", "Launch"))
        self.assertSuccessfulRoute(
            plain_route, " Get all launch post with plain text formatting")
        json_route = (Routes['posts'] + "/{}/{}/{}/json"
                      .format(year_with_posts, "20160422", "Launch"))
        self.assertSuccessfulRoute(
            json_route, " Get all launch post with json formatting")

    def testOtherPages(self):

        # test other routes that do not need parameters beside just a year
        other_routes = [
            'fieldsrulespage',
            'homepage',
            'schedulepage',
            'standingspage',
            'statspage',
            'leagueleaderpage',
            'alltimeleaderspage',
            'eventspage',
            'espysbreakdown',
            'sponsorbreakdown'
        ]
        current_year = datetime.now().year
        for route in other_routes:
            actual_route = Routes[route] + "/{}".format(current_year)
            error_message = ("expecting 200 for route: {} page at url: {}"
                             .format(route, Routes[route]))
            self.assertSuccessfulRoute(actual_route, error_message)

    def assertSuccessfulRoute(self,
                              route,
                              assert_message,
                              expect_status=SUCCESSFUL_GET_CODE):
        with self.app.get(route) as result:
            self.assertEqual(expect_status, result.status_code, assert_message)
