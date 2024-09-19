import pytest
from flask import url_for
from datetime import datetime
from api.models.shared import split_datetime
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_able_get_one_team_stats(
    mlsb_app,
    client,
    team_factory,
    sponsor_factory,
    league_factory,
    division_factory,
    game_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        division = division_factory()
        team = team_factory(sponsor=sponsor_factory(), league=league)
        other_team = team_factory(sponsor=sponsor_factory(), league=league)
        game_date, _ = split_datetime(datetime.today())

        game_factory(
            team,
            other_team,
            league,
            division,
            date=game_date,
            time='10:00'
        )
        url = url_for("rest.team_stats")
        response = client.post(url, data={'team_id': team.id}, follow_redirects=True)
        assert response.status_code == 200
        data = loads(response.data)
        print(data)
        assert len(data) == 1
        assert data[0]['team_id'] == team.id


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_able_get_multiple_team_stats(
    mlsb_app,
    client,
    team_factory,
    sponsor_factory,
    league_factory,
    division_factory,
    game_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        division = division_factory()
        team = team_factory(sponsor=sponsor_factory(), league=league)
        other_team = team_factory(sponsor=sponsor_factory(), league=league)
        game_date, _ = split_datetime(datetime.today())

        game_factory(
            team,
            other_team,
            league,
            division,
            date=game_date,
            time='10:00'
        )
        url = url_for("rest.team_stats")
        response = client.post(url, data={'league_id': league.id}, follow_redirects=True)
        assert response.status_code == 200
        data = loads(response.data)
        assert len(data) == 2
