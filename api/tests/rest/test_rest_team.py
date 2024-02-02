import pytest
from flask import url_for
from datetime import date
from api.tests.fixtures import random_name
from api.model import Team
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
def test_able_create_team(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    league_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = random_name("Color")
        response = client.post(
            url_for("rest.teams"),
            json={
                "color": color,
                "sponsor_id": sponsor.id,
                "league_id": league.id,
                'year': date.today().year
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['color'] == color
        assert data['sponsor_id'] == sponsor.id
        assert data['league_id'] == league.id
        assert data['year'] == date.today().year
        assert isinstance(data['team_id'], int) is True
        assert Team.does_team_exist(data['team_id']) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
def test_required_fields_of_team(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory
):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        color = random_name("Color")
        response = client.post(
            url_for("rest.teams"),
            json={
                "color": color,
                "sponsor_id": sponsor.id,
                'year': date.today().year
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 400


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('team_factory')
def test_update_team(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    league_factory,
    team_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = random_name("Color")
        new_color = random_name("New Color")
        team = team_factory(color=color, sponsor=sponsor, league=league)
        response = client.put(
            url_for("rest.team", team_id=team.id),
            json={
                "color": new_color,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['color'] == new_color
        assert Team.query.filter(Team.color == new_color).first is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('team_factory')
def test_delete_team(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    league_factory,
    team_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = random_name("Color")
        team = team_factory(color=color, sponsor=sponsor, league=league)
        response = client.delete(
            url_for("rest.team", team_id=team.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        assert Team.does_team_exist(sponsor.id) is False


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_get_all_team(
    mlsb_app,
    client,
    admin_header
):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.teams"),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert 'items' in data
        assert 'next_url' in data
        assert isinstance(data['items'], list) is True


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('team_factory')
def test_get_team(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    league_factory,
    team_factory,
    player_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = random_name("Color")
        captain = player_factory()
        year = date.today().year
        team = team_factory(
            color=color,
            sponsor=sponsor,
            league=league,
            captain=captain,
            year=year
        )
        response = client.get(
            url_for("rest.team", team_id=team.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['team_id'] == team.id
        assert data['sponsor_id'] == sponsor.id
        assert data['team_name'] == str(team)
        assert data['color'] == color
        assert data['espys'] == 0
        assert data['league_id'] == league.id
        assert data['year'] == year
        assert 'captain' in data
        assert data['captain']['player_id'] == captain.id
