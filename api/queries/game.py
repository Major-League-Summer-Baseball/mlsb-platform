from datetime import date, datetime, time, timedelta
from api.models.game import Bat
from api.models.league import Division, League
from api.models.player import Player
from api.models.team import Team
from api.extensions import DB
from api.model import Game

def game_summary(
    game_id=None,
    league_id=None,
    division_id=None,
    year=None,
    today=False,
    increment=None
):
    result = []
    if game_id is not None:
        games = DB.session.query(Game).filter_by(id=game_id)
    else:
        t1 = time(0, 0)
        t2 = time(23, 59)
        if year is not None:
            d1 = date(year, 1, 1)
            d2 = date(year, 12, 30)
        else:
            d1 = date(2014, 1, 1)
            d2 = date(date.today().year, 12, 30)
        if today:
            d1 = date.today() + timedelta(-2)
            d2 = date.today() + timedelta(2)
        if increment is not None:
            d1 = date.today() + timedelta(-increment)
            d2 = date.today() + timedelta(increment)
        start = datetime.combine(d1, t1)
        end = datetime.combine(d2, t2)
        games = (DB.session.query(Game)
                 .filter(Game.date.between(start, end))
                 .order_by(Game.date))
    if division_id is not None:
        games = games.filter_by(division_id=division_id)
    if league_id is not None:
        games = games.filter_by(league_id=league_id)
    for game in games:
        aid = game.away_team_id
        hid = game.home_team_id
        if aid is None or hid is None:
            break
        g = {
            'status': game.status,
            'game_id': game.id,
            'home_score': 0,
            'away_score': 0,
            'home_bats': [],
            'away_bats': [],
            'home_team': None,
            'away_team': None,
            'date': game.date.strftime("%Y-%m-%d %H:%M"),
            'league': League.query.get(game.league_id).json(),
            'division': Division.query.get(game.division_id).json()
        }
        g['home_team'] = Team.query.get(hid).json()
        g['away_team'] = Team.query.get(aid).json()
        away_bats = (DB.session.query(Bat,
                                      Player)
                     .join(Player)
                     .filter(Bat.team_id == aid)
                     .filter(Bat.game_id == game.id)
                     ).all()
        home_bats = (DB.session.query(Bat,
                                      Player)
                     .join(Player)
                     .filter(Bat.team_id == hid)
                     .filter(Bat.game_id == game.id)
                     ).all()
        for bat in away_bats:
            g['away_bats'].append({'name': bat[1].name,
                                   'hit': bat[0].classification,
                                   'inning': bat[0].inning,
                                   'rbi': bat[0].rbi,
                                   'bat_id': bat[0].id})
            g['away_score'] += bat[0].rbi
        for bat in home_bats:
            g['home_bats'].append({'name': bat[1].name,
                                   'hit': bat[0].classification,
                                   'inning': bat[0].inning,
                                   'rbi': bat[0].rbi,
                                   'bat_id': bat[0].id})
            g['home_score'] += bat[0].rbi
        if g['away_bats'] == 0:
            g['away_score'] = "--"
        if g['home_bats'] == 0:
            g['home_score'] = "--"
        result.append(g)
    return result