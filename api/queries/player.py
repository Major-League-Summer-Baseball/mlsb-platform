from datetime import datetime, date, time
from sqlalchemy.sql import func, not_
from api.extensions import DB
from api.model import Player, Bat, Game
from api.variables import UNASSIGNED_EMAIL


def player_summary(year=None, team_id=None, league_id=None, player_id=None):
    bats = func.count(Bat.classification).label('bats')
    rbi = func.count(Bat.rbi).label('rbis')
    if year is not None:
        d1 = date(year, 1, 1)
        t = time(0, 0)
        d2 = date(year, 12, 30)
    else:
        d1 = date(2014, 1, 1)
        t = time(0, 0)
        d2 = date(date.today().year, 12, 30)
    start = datetime.combine(d1, t)
    end = datetime.combine(d2, t)
    players = (DB.session.query(Player.name,
                                Bat.classification,
                                bats,
                                Player.id,
                                rbi)
               .join(Player.bats)
               .join(Game)
               .filter(Game.date.between(start, end))
               .filter(not_(Player.email.ilike(UNASSIGNED_EMAIL))))
    if team_id is not None:
        players = players.filter(Bat.team_id == team_id)
    if league_id is not None:
        players = players.filter(Game.league_id == league_id)
    if player_id is not None:
        players = players.filter(Player.id == player_id)
    players = (players
               .group_by(Bat.classification)
               .group_by(Player.id))
    players = players.all()
    result = {}
    for player in players:
        # format the results
        if player[3] not in result.keys():
            result[player[3]] = {
                's': 0,
                'd': 0,
                'hr': 0,
                'ss': 0,
                'k': 0,
                'fo': 0,
                'fc': 0,
                'e': 0,
                'go': 0,
                'id': player[3],
                'rbi': 0,
                'bats': 0,
                'avg': 0.000,
                'name': player[0]
            }
        result[player[3]][player[1]] = player[2]
        result[player[3]]['rbi'] += player[4]
    final_result = {}
    for player in result:
        # calculate the bats and average
        result[player]['bats'] = (result[player]['s'] +
                                  result[player]['ss'] +
                                  result[player]['d'] +
                                  result[player]['hr'] +
                                  result[player]['k'] +
                                  result[player]['fo'] +
                                  result[player]['fc'] +
                                  result[player]['e'] +
                                  result[player]['go']
                                  )
        bats = max(result[player]['bats'], 1)
        result[player]['avg'] = round(((result[player]['s'] +
                                        result[player]['ss'] +
                                        result[player]['d'] +
                                        result[player]['hr']) /
                                       result[player]['bats']), 3)
        player_name = result[player].pop('name', None)
        final_result[player_name] = result[player]
    return final_result
