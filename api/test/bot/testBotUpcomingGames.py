from base64 import b64encode
from api.helper import loads
from api.routes import Routes
from api.model import Team
from api.test.BaseTest import \
    TestSetup, ADMIN, PASSWORD, INVALID_ID, \
    addGame, SUCCESSFUL_GET_CODE
from api.errors import PlayerDoesNotExist
import datetime
headers = {
    'Authorization': 'Basic %s' % b64encode(bytes(ADMIN + ':' +
                                                  PASSWORD, "utf-8")
                                            ).decode("ascii")
}


class testUpcomingGames(TestSetup):

    def testMain(self):
        app = self.getApp()
        with app.app_context(), app.test_request_context():
            # non-subscribed player
            day = datetime.date.today() + datetime.timedelta(days=1)
            game = addGame(self, day=day.strftime("%Y-%m-%d"), time="22:40")
            team_model = Team.query.get(game['home_team_id'])
            team = team_model.json()
            player = self.add_player("Test Bot Captain", "testbot@mlsb.ca", "m")
            self.add_player_to_team(team, player, captain=True)
            route = Routes['botupcominggames']

            # invalid player id
            data = {'player_id': INVALID_ID}
            expect = {
                'details': INVALID_ID,
                'message': PlayerDoesNotExist.message
            }
            rv = self.app.post(route, json=data, headers=headers)
            self.output(loads(rv.data))
            self.output(expect)
            error = route + " POST: Player DNE for upcoming games"
            self.assertEqual(rv.status_code, PlayerDoesNotExist.status_code, error)
            self.assertEqual(expect, loads(rv.data), error)

            # subscribed player upcoming games
            data = {'player_id': player['player_id']}
            expect = [
                {
                    'away_team': game['away_team'],
                    'away_team_id': game['away_team_id'],
                    'date': game['date'],
                    'field': game['field'],
                    'game_id': game['game_id'],
                    'home_team': game['home_team'],
                    'home_team_id': game['home_team_id'],
                    'league_id': game['league_id'],
                    'division_id': game['division_id'],
                    'status': game['status'],
                    'time': game['time']
                }
            ]
            rv = self.app.post(
                Routes['botupcominggames'], json=data, headers=headers
            )
            self.output(loads(rv.data))
            self.output(expect)
            error = route + " POST: Subscribed player for upcoming games"
            self.assertEqual(rv.status_code, SUCCESSFUL_GET_CODE, error)
            self.assertEqual(expect, loads(rv.data), error)
