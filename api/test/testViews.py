from flask import url_for
from api.test.BaseTest import \
    TestSetup, SUCCESSFUL_GET_CODE, INVALID_ID, REDIRECT_CODE
from datetime import datetime
import uuid


START_OF_PLATFORM = 2016
YEAR_WITH_NO_DATA = 1992


class TestWebsiteViews(TestSetup):

    def testStaticFileNotYearSpecific(self):
        # pages that do not need a year
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            self.assertGetRequest(
                url_for('website.mlsb_logo'),
                "Logo page should give a 200"
            )
            self.assertGetRequest(
                url_for('website.privacy_policy'),
                "Privacy page should give a 200"
            )

    def testLoginPages(self):
        self.assertGetRequest("/authenticate", "Need to login")
        self.assertGetRequest("/login", "Login page")
        self.assertGetRequest("/request_sent", "League request sent page")

    def testSponsorsPages(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            sponsor_name = str(uuid.uuid1())
            sponsor = self.add_sponsor(sponsor_name)
            current_year = current_year = datetime.now().year
            # get the sponsor picture using sponsor name or id
            self.assertGetRequest(
                url_for('website.sponsor_picture', name=sponsor_name),
                "Get sponsor picture from name"
            )
            self.assertGetRequest(
                url_for('website.sponsor_picture', name=sponsor['sponsor_id']),
                "Get sponsor picture from id"
            )

            # get the sponsor page for all sponsors for a specific sponsor
            self.assertGetRequest(
                url_for(
                    'website.sponsors_page',
                    year=current_year,
                    name=INVALID_ID
                ),
                "Get a page of all the sponsors"
            )
            self.assertGetRequest(
                url_for(
                    'website.sponsor_page',
                    year=current_year,
                    sponsor_id=sponsor['sponsor_id']
                ),
                "Get a page of specific sponsor"
            )

            # get a non-existent sponsor
            self.assertGetRequest(
                url_for('website.sponsor_picture', name=str(uuid.uuid1())),
                "Get non-existent sponsor picture"
            )
            self.assertGetRequest(
                url_for('website.sponsor_picture', name=INVALID_ID),
                "Get sponsor picture from id"
            )
            self.assertGetRequest(
                url_for(
                    'website.sponsors_page',
                    year=current_year,
                    name=INVALID_ID
                ),
                "Get a page of non-existent sponsor"
            )

    def testTeamPages(self):
        current_year = datetime.now().year
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # test team with a sponsor
            sponsor = self.add_sponsor(str(uuid.uuid1()))
            league = self.add_league(str(uuid.uuid1()))
            team_with_sponsor = self.add_team(
                "white", sponsor=sponsor, league=league)
            self.assertGetRequest(
                url_for('website.team_picture', team=team_with_sponsor['team_id']),
                "Get picture of team with a sponsor"
            )
            team_id = team_with_sponsor['team_id']
            self.assertGetRequest(
                url_for('website.team_page', year=current_year, team_id=team_id),
                "Get page of team with a sponsor"
            )

            # test non-existent team
            self.assertGetRequest(
                url_for('website.team_picture', team=INVALID_ID),
                "Get picture of non-existent team"
            )
            self.assertGetRequest(
                url_for('website.team_page', year=current_year, team_id=INVALID_ID),
                "Get page of non-existent team"
            )

    def testPlayerPage(self):
        current_year = datetime.now().year
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # test player
            player_name = str(uuid.uuid1())
            player = self.add_player(
                player_name, player_name + "@mlsb.ca", gender="F"
            )
            self.assertGetRequest(
                url_for(
                    'website.player_page',
                    year=current_year,
                    player_id=player['player_id']
                ),
                'Get page of a player'
            )

            # test non-existent player
            self.assertGetRequest(
                url_for(
                    'website.player_page',
                    year=current_year,
                    player_id=INVALID_ID
                ),
                'Get page of a non-existent player'
            )

    def testPostPages(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # get all the posts
            self.assertGetRequest(
                url_for('website.posts_json', year=START_OF_PLATFORM),
                " Get all the posts descriptions"
            )

            # render the template for some post
            route = url_for(
                'website.checkout_post',
                year=START_OF_PLATFORM,
                date='20160422',
                file_name='Launch.html'
            )
            error_message = "Get launch post at {}".format(route)
            self.assertGetRequest(route, error_message)

            # get one of the post pictures
            route = url_for('website.post_picture', name='bot.png')
            message = "Get post picture at {}".format(route)
            self.assertGetRequest(route, message)

            # get a post pictures that does not exist
            route = url_for('website.post_picture', name='picDoesNotExist.png')
            message = ("Get non-existent post picture at {}".format(route))
            # will send back not found png
            self.assertGetRequest(
                url_for('website.post_picture', name='picDoesNotExist.png'), message
            )

            # get a single post plain or json format
            for route in [
                url_for(
                    'website.checkout_post_raw_html',
                    year=START_OF_PLATFORM,
                    date='20160422',
                    file_name='Launch.html'
                ),
                url_for(
                    'website.checkout_post_json',
                    year=START_OF_PLATFORM,
                    date='20160422',
                    file_name='Launch.html'
                ),
            ]:
                message = "Get launch post with formatting at {}".format(route)
                self.assertGetRequest(route, message)

    def testHomepagePosts(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # homepage with posts
            self.assertGetRequest(
                url_for('website.index', year=START_OF_PLATFORM),
                "Get homepage with summaries"
            )

            # homepage without posts
            self.assertGetRequest(
                url_for('website.index', year=YEAR_WITH_NO_DATA),
                "Get homepage without summaries"
            )

    def testEventsPages(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # year with events
            self.assertGetRequest(
                url_for('website.events_page', year=START_OF_PLATFORM),
                "Get events for a given year"
            )

            # year with no events
            self.assertGetRequest(
                url_for('website.events_page', year=YEAR_WITH_NO_DATA),
                "Get events for a given year with no events"
            )

    def testLeaguePages(self):
        # test the pages that are dependent on a league
        current_year = datetime.now().year
        app = self.getApp()
        expected_codes = [SUCCESSFUL_GET_CODE, REDIRECT_CODE]
        with app.app_context(), app.test_request_context():
            routes = []
            for league_id in range(1, 10):
                routes.append(
                    url_for('website.schedule', year=current_year, league_id=league_id)
                )
                routes.append(
                    url_for('website.standings', year=current_year, league_id=league_id)
                )
            for route in routes:
                with self.app.get(route) as result:
                    message = "expect 200 for url: {}".format(route)
                    self.assertTrue(
                        result.status_code in expected_codes,
                        message
                    )

    def testOtherPages(self):
        # test other routes that do not need parameters beside just a year
        current_year = datetime.now().year
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            for route in [
                url_for('website.rules_fields', year=current_year),
                url_for('website.index', year=current_year),
                url_for('website.stats_page', year=current_year),
                url_for('website.leaders_page', year=current_year),
                url_for('website.all_time_leaders_page', year=current_year),
                url_for('website.events_page', year=current_year),
                url_for('website.espys_breakdown_request', year=current_year),
                url_for('website.sponsor_breakdown', year=current_year),
                url_for('website.promos_page', year=current_year)
            ]:
                error_message = "Expecting 200 at url: {}".format(route)
                self.assertGetRequest(route, error_message)

    def assertGetRequest(self,
                         route,
                         assert_message,
                         expected_status=SUCCESSFUL_GET_CODE):
        with self.app.get(route) as result:
            self.assertEqual(expected_status, result.status_code,
                             assert_message)
