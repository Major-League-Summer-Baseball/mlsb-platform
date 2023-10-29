from flask import url_for
from api.test.BaseTest import TestSetup, SUCCESSFUL_GET_CODE
START_OF_PLATFORM = 2016
YEAR_WITH_NO_DATA = 1992


class TestDocumentation(TestSetup):

    def testStaticDocumetnationFiles(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            documentation_routes = [
                url_for('index_doc'),
                url_for('response_object_doc'),
                url_for('player_object_doc'),
                url_for('team_object_doc'),
                url_for('bat_object_doc'),
                url_for('game_object_doc'),
                url_for('league_object_doc'),
                url_for('league_event_object_doc'),
                url_for('league_event_date_object_doc'),
                url_for('division_object_doc'),
                url_for('sponsor_object_doc'),
                url_for('fun_object_doc'),
                url_for('pagination_object_doc'),
                url_for('teamroster_object_doc'),
                url_for('teamroster_route_doc'),
                url_for('fun_route_doc'),
                url_for('team_route_doc'),
                url_for('player_route_doc'),
                url_for('bat_route_doc'),
                url_for('game_route_doc'),
                url_for('sponsor_route_doc'),
                url_for('league_route_doc'),
                url_for('league_event_route_doc'),
                url_for('league_event_dateroute_doc'),
                url_for('division_route_doc'),
                url_for('team_view_doc'),
                url_for('game_view_doc'),
                url_for('league_event_view_doc'),
                url_for('player_view_doc'),
                url_for('fun_meter_view_doc'),
                url_for('player_lookup_view_doc'),
                url_for('player_team_lookup_view_doc'),
                url_for('league_leaders_view_doc'),
                url_for('schedule_view_doc'),
                url_for('divisions_view_doc'),
                url_for('authenticate_bot_doc'),
                url_for('submit_score_bot_doc'),
                url_for('upcoming_games_bot_doc'),
                url_for('captain_games_bot_doc'),
                url_for('submit_transaction_bot_doc'),
            ]
            for route in documentation_routes:
                with self.app.get(route) as result:
                    message = "Unable to get docs for {}".format(route)
                    self.assertEqual(
                        SUCCESSFUL_GET_CODE,
                        result.status_code,
                        message
                    )
