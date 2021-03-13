'''
@author: Dallas Fraser
@author: 2019-03-13
@organization: MLSB API
@summary: Tests some views at least do not respond with application error
'''
from api.routes import Routes
from api.test.BaseTest import TestSetup, SUCCESSFUL_GET_CODE, INVALID_ID,\
    NOT_FOUND_CODE, REDIRECT_CODE
from datetime import datetime
import uuid
START_OF_PLATFORM = 2016
YEAR_WITH_NO_DATA = 1992


class TestWebsiteViews(TestSetup):

    def testStaticFileNotYearSpecific(self):
        # pages that do not need a year
        self.assertGetRequest(Routes['logo'],
                              "Logo page should give a 200")
        self.assertGetRequest(Routes['privacy'],
                              "Privacy page should give a 200")

    def testSponsorsPages(self):
        sponsor_name = str(uuid.uuid1())
        sponsor = self.add_sponsor(sponsor_name)

        # get the sponsor picture using sponsor name or id
        route = Routes['sponsorspicture'] + "/{}".format(sponsor_name)
        self.assertGetRequest(route, "Get sponsor picture from name")
        route = Routes['sponsorspicture'] + "/{}".format(sponsor['sponsor_id'])
        self.assertGetRequest(route, "Get sponsor picture from id")

        # get the sponsor page for all sponsors for a specific sponsor
        current_year = current_year = datetime.now().year
        route = Routes['sponsorspage'] + "/{}".format(current_year)
        self.assertGetRequest(route, "Get a page of all the sponsors")
        route = Routes['sponsorspage'] + "/{}/{}".format(current_year,
                                                         sponsor['sponsor_id'])
        self.assertGetRequest(route, "Get a page of specific sponsor")

        # get a non-existent sponsor
        route = Routes['sponsorspicture'] + "/{}".format(str(uuid.uuid1()))
        self.assertGetRequest(route, "Get non-existent sponsor picture")
        route = Routes['sponsorspicture'] + "/{}".format(INVALID_ID)
        self.assertGetRequest(route, "Get sponsor picture from id")
        route = Routes['sponsorspage'] + "/{}/{}".format(current_year,
                                                         INVALID_ID)
        self.assertGetRequest(route, "Get a page of non-existent sponsor")

    def testTeamPages(self):
        current_year = datetime.now().year

        # test team with a sponsor
        sponsor = self.add_sponsor(str(uuid.uuid1()))
        league = self.add_league(str(uuid.uuid1()))
        team_with_sponsor = self.add_team(
            "white", sponsor=sponsor, league=league)
        route = (Routes['teampicture'] +
                 "/{}".format(team_with_sponsor['team_id']))
        self.assertGetRequest(route,
                              "Get picture of team with a sponsor")
        route = (Routes['teampage'] +
                 "/{}/{}".format(current_year, team_with_sponsor['team_id']))
        self.assertGetRequest(route,
                              "Get page of team with a sponsor")

        # test non-existent team
        route = Routes['teampicture'] + "/{}".format(INVALID_ID)
        self.assertGetRequest(route,
                              "Get picture of non-existent team")
        route = Routes['teampage'] + "/{}/{}".format(current_year, INVALID_ID)
        self.assertGetRequest(route,
                              "Get page of non-existent team")

    def testPlayerPage(self):
        current_year = datetime.now().year

        # test player
        player_name = str(uuid.uuid1())
        player = self.add_player(
            player_name, player_name + "@mlsb.ca", gender="F")
        route = Routes['playerpage'] +\
            "/{}/{}".format(current_year, player['player_id'])
        self.assertGetRequest(route, 'Get page of a player')

        # test non-existent player
        route = Routes['playerpage'] +\
            "/{}/{}".format(current_year, INVALID_ID)
        self.assertGetRequest(route, 'Get page of a non-existent player')

    def testPostPages(self):
        # get all the posts
        route = Routes['posts'] + "/{}".format(START_OF_PLATFORM)
        self.assertGetRequest(route, " Get all the posts descriptions")

        # render the template for some post
        route = (Routes['posts'] + "/{}/{}/{}".format(START_OF_PLATFORM,
                                                      "20160422",
                                                      "Launch.html"))
        error_message = ("Get launch post at {}"
                         .format(route))
        self.assertGetRequest(route, error_message)

        # get one of the post pictures
        route = (Routes['postpicture'] + "/{}".format('bot.png'))
        error_message = ("Get post picture at {}"
                         .format(route))
        self.assertGetRequest(route, error_message)

        # get a post pictures that does not exist
        route = (Routes['postpicture'] + "/{}".format('picDoesNotExist.png'))
        error_message = ("Get non-existent post picture at {}"
                         .format(route))
        self.assertGetRequest(route, error_message,
                              expected_status=NOT_FOUND_CODE)

        # get a single post plain or json format
        for extension in ["plain", "json"]:
            route = (Routes['posts'] + "/{}/{}/{}/{}".format(START_OF_PLATFORM,
                                                             "20160422",
                                                             "Launch.html",
                                                             extension))
            error_message = ("Get launch post with formatting {} at {}"
                             .format(extension, route))
            self.assertGetRequest(route, error_message)

    def testHomepagePosts(self):
        # homepage with posts
        route = Routes['homepage'] + "/{}".format(START_OF_PLATFORM)
        error_message = "Get homepage with summaries"
        self.assertGetRequest(route, error_message)

        # homepage without posts
        route = Routes['homepage'] + "/{}".format(YEAR_WITH_NO_DATA)
        error_message = "Get homepage without summaries"
        self.assertGetRequest(route, error_message)

    def testEventsPages(self):

        # year with events
        route = Routes['eventspage'] + "/{}".format(START_OF_PLATFORM)
        error_message = "Get events for a given year"
        self.assertGetRequest(route, error_message)

        # year with no events
        route = Routes['eventspage'] + "/{}".format(YEAR_WITH_NO_DATA)
        error_message = "Get events for a given year with no events"
        self.assertGetRequest(route, error_message)

    def testLeaguePages(self):
        # test the pages that are dependent on a league
        league_routes = [
            'schedulepage',
            'standingspage',
        ]
        current_year = datetime.now().year
        for route in league_routes:
            for division in range(1, 10):
                actual_route = Routes[route] + f"/{division}/{current_year}"
                error_message = ("expecting 200 for route: {} page at url: {}"
                                 .format(route, Routes[route]))
                with self.app.get(actual_route) as result:
                    self.assertTrue(result.status_code in [SUCCESSFUL_GET_CODE,
                                                           REDIRECT_CODE],
                                    error_message)

    def testOtherPages(self):

        # test other routes that do not need parameters beside just a year
        other_routes = [
            'fieldsrulespage',
            'homepage',
            'statspage',
            'leagueleaderpage',
            'alltimeleaderspage',
            'eventspage',
            'espysbreakdown',
            'sponsorbreakdown',
            'promos'
        ]
        current_year = datetime.now().year
        for route in other_routes:
            actual_route = Routes[route] + "/{}".format(current_year)
            error_message = ("expecting 200 for route: {} page at url: {}"
                             .format(route, Routes[route]))
            self.assertGetRequest(actual_route, error_message)

    def assertGetRequest(self,
                         route,
                         assert_message,
                         expected_status=SUCCESSFUL_GET_CODE):
        with self.app.get(route) as result:
            self.assertEqual(expected_status, result.status_code,
                             assert_message)
