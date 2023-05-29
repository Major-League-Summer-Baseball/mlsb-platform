'''
@author: Dallas Fraser
@author: 2016-04-12
@organization: MLSB API
@summary: The views for player stats
'''
from flask_restful import Resource, reqparse
from flask import Response
from json import dumps
from api.model import LeagueEvent, LeagueEventDate
from datetime import datetime, date, time
parser = reqparse.RequestParser()
parser.add_argument('year', type=int)


def get_year_events(year: int) -> list[dict]:
    """ Get a list of the given year events """
    active = LeagueEvent.query.filter(LeagueEvent.active == True).all()

    # all events with a current date
    year_start = datetime.combine(date(year, 1, 1), time(0, 0))
    year_end = datetime.combine(date(year, 12, 30), time(0, 0))
    dates = LeagueEventDate.query.filter(LeagueEventDate.date.between(year_start, year_end)).all()
    events = [date.json() for date in dates]
    event_ids = [date.league_event_id for date in dates]

    # add events that are missing a date
    for event in active:
        if event.id not in event_ids:
            event_info = event.json()
            event_info['league_event_date_id'] = None
            event_info['date'] = "TBD"
            event_info['time'] = "TBD"
            event_info['attendance'] = 0
            events.append(event_info)
    return events


class LeagueEventViewAPI(Resource):

    def get(self, year):
        """
            GET request for for this year events
            Route: Route['vleagueevents']/<year>
            Parameters:
                year: the year  (int)
            Returns:
                status: 200
                mimetype: application/json
                data: list of LeagueEventDate (with TBD if not date)
        """
        return Response(dumps(get_year_events(year)),
                        status=200,
                        mimetype="application/json")
