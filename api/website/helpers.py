# -*- coding: utf-8 -*-
""" Some helper functions for various pages. """
from api.extensions import DB
from api.model import Team, Player, League
from api.models.sponsor import Sponsor
from api.queries.player import player_summary
from api.cached_items import single_team


def get_team(year, team_id: int) -> dict:
    """Get the team record and player stats for a given team."""
    result = Team.query.get(team_id)
    team = None
    if result is not None:
        captain = "TBD" if result.player_id is None else str(
            Player.query.get(result.player_id)
        )
        p_ = player_summary(team_id=team_id)
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
                'sp': "{0:.3f}".format(sp)
            })
        record = single_team(team_id)
        league_name = "No league"
        if result.league_id is not None:
            league_name = str(League.query.get(result.league_id))
        team = {
            'name': str(result),
            'league': league_name,
            'captain': str(captain),
            'captain_id': result.player_id,
            'players': [player.json() for player in result.players],
            'record': record,
            'wins': record['wins'],
            'losses': record['losses'],
            'ties': record['ties'],
            'stats': stats,
            'image_id': result.image_id,
            'image': None if result.image_id is None else result.image.json(),
        }
    return team


def get_teams(year: int) -> list:
    """Get a list of teams for the given year."""
    result = (
        DB.session
        .query(Team)
        .outerjoin(Sponsor)
        .filter(Team.year == year)
        .order_by(Sponsor.name).all()
    )
    return [{'id': team.id, 'name': str(team)} for team in result]
