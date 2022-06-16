# -*- coding: utf-8 -*-
""" Some helper functions for various pages. """
from api import DB
from api.model import Team, Player, Sponsor, League
from api.advanced.players_stats import post as player_summary
from api.cached_items import single_team


def get_team(year, tid: int) -> dict:
    result = Team.query.get(tid)
    team = None
    if result is not None:
        captain = "TBD"
        players = []
        for player in result.players:
            if player.name not in players:
                players.append(player.json())
        if result.player_id is not None:
            captain = str(Player.query.get(result.player_id))
        p_ = player_summary(team_id=tid)
        stats = []
        for name in p_:
            sp = (
                (
                    p_[name]["s"] +
                    p_[name]["ss"] +
                    p_[name]["d"] * 2 +
                    p_[name]["hr"] * 4
                ) / p_[name]['bats']
            )
            stats.append({
                'id': p_[name]['id'],
                'name': name,
                'ss': p_[name]['ss'],
                's': p_[name]['s'],
                'd': p_[name]['d'],
                'hr': p_[name]['hr'],
                'bats': p_[name]['bats'],
                'ba': "{0:.3f}".format(p_[name]['avg']),
                'sp': "{0:.3f}".format(sp)})
        record = single_team(tid)
        team = {'name': str(result),
                'league': str(League.query.get(result.league_id)),
                'captain': str(captain),
                'captain_id': result.player_id,
                'players': players,
                'record': record,
                'wins': record[tid]['wins'],
                'losses': record[tid]['losses'],
                'ties': record[tid]['ties'],
                'stats': stats}
    return team


def get_teams(year: int) -> list:
    result = (DB.session.query(Team.id, Team.color, Sponsor.nickname)
              .join(Sponsor)
              .filter(Team.year == year)
              .order_by(Sponsor.nickname).all())
    teams = []
    for team in result:
        if (team[2] is None):
            name = team[1]
        else:
            name = team[2] + " " + team[1]
        teams.append({'id': team[0],
                      'name': name})
    return teams
