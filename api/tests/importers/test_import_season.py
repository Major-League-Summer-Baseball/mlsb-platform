from typing import List
import pytest
import logging
from api.importers.season import create_team_season, TeamInfo, TeamGamesScore


def assert_season_matches_record(
    team: TeamInfo, season: List[TeamGamesScore]
):
    runs_for = 0
    runs_against = 0
    wins = 0
    losses = 0
    ties = 0
    for game in season:
        runs_for += game['score']
        runs_against += game['other_score']
        if game['score'] > game['other_score']:
            wins += 1
        elif game['score'] < game['other_score']:
            losses += 1
        else:
            ties += 1

    assert team['record']['wins'] == wins
    assert team['record']['losses'] == losses
    assert team['record']['ties'] == ties
    assert team['record']['runs_for'] == runs_for
    assert team['record']['runs_allowed'] == runs_against
    for player in team['homeruns']:
        player_homeruns = 0
        for game in season:
            player_homeruns += len([
                hr
                for hr in game['homeruns']
                if hr == player['player'].id
            ])
        assert player['homeruns'] == player_homeruns
    for player in team['singles']:
        player_singles = 0
        for game in season:
            player_singles += len([
                hr
                for hr in game['singles']
                if hr == player['player'].id
            ])
        assert player['singles'] == player_singles


@pytest.mark.parametrize("record", [
    {
        'wins': 5,
        'losses': 5,
        'ties': 1,
        'runs_for': 11,
        'runs_allowed': 11,
        'espys': 1,
    },
    {
        'wins': 10,
        'losses': 0,
        'ties': 1,
        'runs_for': 11,
        'runs_allowed': 1,
        'espys': 1,
    },
    {
        'wins': 0,
        'losses': 10,
        'ties': 1,
        'runs_for': 1,
        'runs_allowed': 11,
        'espys': 1,
    },
    {
        'wins': 11,
        'losses': 0,
        'ties': 0,
        'runs_for': 11,
        'runs_allowed': 0,
        'espys': 1,
    },
    {
        'wins': 0,
        'losses': 11,
        'ties': 0,
        'runs_for': 0,
        'runs_allowed': 11,
        'espys': 1,
    },
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_create_team_season(
    record,
    mlsb_app,
    sponsor_factory,
    team_factory,
    league_factory,
):
    with mlsb_app.app_context():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        logger = logging.getLogger(__name__)
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league
        )
        team_info = {
            'team': home_team,
            'record': record,
            'homeruns': [],
            'singles': []
        }
        season = create_team_season(team_info, logger)
        assert_season_matches_record(team_info, season)


@pytest.mark.parametrize("record", [
    {
        'wins': 10,
        'losses': 0,
        'ties': 1,
        'runs_for': 22,
        'runs_allowed': 1,
        'espys': 1,
    },
    {
        'wins': 0,
        'losses': 10,
        'ties': 1,
        'runs_for': 22,
        'runs_allowed': 44,
        'espys': 1,
    },
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_create_team_homeruns_and_singles(
    record,
    mlsb_app,
    sponsor_factory,
    player_factory,
    team_factory,
    league_factory,
):
    with mlsb_app.app_context():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        player = player_factory()
        logger = logging.getLogger(__name__)
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league
        )
        team_info = {
            'team': home_team,
            'record': record,
            'homeruns': [{
                'player': player,
                'homeruns': 18,
                'singles': 18
            }],
            'singles': []
        }
        season = create_team_season(team_info, logger)
        assert_season_matches_record(team_info, season)