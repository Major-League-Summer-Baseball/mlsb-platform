from datetime import datetime, date, time
from api.model import LeagueEvent, LeagueEventDate

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