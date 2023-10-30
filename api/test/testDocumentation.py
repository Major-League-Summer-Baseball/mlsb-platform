from flask import url_for
from api.test.BaseTest import TestSetup, SUCCESSFUL_GET_CODE
START_OF_PLATFORM = 2016
YEAR_WITH_NO_DATA = 1992


class TestDocumentation(TestSetup):

    def testStaticDocumetnationFiles(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            documentation_routes = [
                url_for('documentation.index_doc'),
                url_for('documentation.response_object_doc'),
                url_for('documentation.player_object_doc'),
                url_for('documentation.team_object_doc'),
                url_for('documentation.bat_object_doc'),
                url_for('documentation.game_object_doc'),
                url_for('documentation.league_object_doc'),
                url_for('documentation.league_event_object_doc'),
                url_for('documentation.league_event_date_object_doc'),
                url_for('documentation.division_object_doc'),
                url_for('documentation.sponsor_object_doc'),
                url_for('documentation.fun_object_doc'),
                url_for('documentation.pagination_object_doc'),
                url_for('documentation.teamroster_object_doc'),
                url_for('documentation.teamroster_route_doc'),
                url_for('documentation.fun_route_doc'),
                url_for('documentation.team_route_doc'),
                url_for('documentation.player_route_doc'),
                url_for('documentation.bat_route_doc'),
                url_for('documentation.game_route_doc'),
                url_for('documentation.sponsor_route_doc'),
                url_for('documentation.league_route_doc'),
                url_for('documentation.league_event_route_doc'),
                url_for('documentation.league_event_dateroute_doc'),
                url_for('documentation.division_route_doc'),
                url_for('documentation.team_view_doc'),
                url_for('documentation.game_view_doc'),
                url_for('documentation.league_event_view_doc'),
                url_for('documentation.player_view_doc'),
                url_for('documentation.fun_meter_view_doc'),
                url_for('documentation.player_lookup_view_doc'),
                url_for('documentation.player_team_lookup_view_doc'),
                url_for('documentation.league_leaders_view_doc'),
                url_for('documentation.schedule_view_doc'),
                url_for('documentation.divisions_view_doc'),
                url_for('documentation.authenticate_bot_doc'),
                url_for('documentation.submit_score_bot_doc'),
                url_for('documentation.upcoming_games_bot_doc'),
                url_for('documentation.captain_games_bot_doc'),
                url_for('documentation.submit_transaction_bot_doc'),
            ]
            for route in documentation_routes:
                with self.app.get(route) as result:
                    message = "Unable to get docs for {}".format(route)
                    self.assertEqual(
                        SUCCESSFUL_GET_CODE,
                        result.status_code,
                        message
                    )
