import pytest
from flask import url_for
from datetime import date, datetime
from api.models.shared import split_datetime
from api.tests.fixtures import random_name
from api.model import Team
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('game_factory')
def test_able_get_schedule(
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
        teams = [
            team_factory(sponsor=sponsor_factory(), league=league),
            team_factory(sponsor=sponsor_factory(), league=league),
            team_factory(sponsor=sponsor_factory(), league=league),
        ]
        game_date, _ = split_datetime(datetime.today())
        
        game_factory(
            teams[0],
            teams[1],
            league,
            division,
            date=game_date,
            time='10:00'
        )
        game_factory(
            teams[0],
            teams[2],
            league,
            division,
            date=game_date,
            time='11:00'
        )
        year = datetime.today().year
        url = url_for("rest.schedule", year=year, league_id=league.id)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = loads(response.data)
        assert len(data['items']) == 2