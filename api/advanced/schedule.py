'''
@author: Dallas Fraser
@date: 2019-03-11
@organization: MLSB API
@summary: The views for game schedule
'''
from flask_restful import Resource, request
from api.cached_items import pull_schedule


class ScheduleAPI(Resource):

    def get(self, year, league_id):
        """
            Get request for schedule data
            Route: Route['vschedule']/<int:year>/<int:team_id>
            Parameters:
                year: the year to get the schedule for
                league_id: the id of the league
            Returns:
                status: 200
                mimetype: application/json
                data: [
                        {
                            "away_team_id": int,
                            "away_team": str,
                            "date": str,
                            "field": str,
                            "home_team_id": int,
                            "home_team": str,
                            "league_id": int,
                            "score": str(home team - away team),
                            "status": str,
                            "time": str
                        }
                    ]
        """
        page = request.args.get('page', 1, type=int)
        return pull_schedule(year, league_id, page=page)
