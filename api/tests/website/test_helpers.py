import pytest
from api.website.helpers import get_teams, get_team
from datetime import date

THIS_YEAR = date.today().year
INVALID_ENTITY = 9999999


@pytest.mark.parametrize("team_data", [
    ('Test Sponsor', "New Color", "Test Sponsor New Color"),
    (None, "Another Color", "Another Color"),
    ("Another Sponsor", None, "Another Sponsor")
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
def test_get_teams(mlsb_app, sponsor_factory, team_factory, team_data):
    with mlsb_app.app_context():
        if team_data[0] is not None:
            sponsor = sponsor_factory(sponsor_name=team_data[0])
            team = team_factory(color=team_data[1], sponsor=sponsor)
        else:
            team = team_factory(color=team_data[1])
        teams = get_teams(THIS_YEAR)
        assert isinstance(teams, list) is True
        find_my_team = [
            my_team for my_team in teams if my_team["id"] == team.id
        ]
        assert len(find_my_team) == 1
        assert find_my_team[0]['name'] == team_data[2]


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_get_team(mlsb_app, team_factory, player_factory, league_factory):
    with mlsb_app.app_context():
        captain = player_factory()
        league = league_factory()
        team = team_factory(league=league, captain=captain)
        result = get_team(THIS_YEAR, team_id=team.id)
        assert result['name'] == str(team)
        assert result['league'] == str(league)
        assert result['wins'] == 0
        assert result['losses'] == 0
        assert result['ties'] == 0
        assert result['captain'] == str(captain)


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_get_team_no_captain(mlsb_app, team_factory, player_factory, league_factory):
    with mlsb_app.app_context():
        league = league_factory()
        team = team_factory(league=league)
        result = get_team(THIS_YEAR, team_id=team.id)
        assert result['name'] == str(team)
        assert result['league'] == str(league)
        assert result['wins'] == 0
        assert result['losses'] == 0
        assert result['ties'] == 0
        assert result['captain'] == "TBD"


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
def test_get_nonexistent_team(mlsb_app):
    with mlsb_app.app_context():
        assert get_team(THIS_YEAR, team_id=INVALID_ENTITY) is None
