import pytest
from flask import url_for
from api.tests.fixtures import random_name
from api.model import Espys
from api.helper import loads


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_able_create_espys(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        team = team_factory(
            random_name('Color'),
            sponsor=sponsor,
            league=league
        )
        description = random_name("Description")
        receipt = random_name("Receipt")
        points = 100
        response = client.post(
            url_for("rest.espys"),
            json={
                "sponsor_id": sponsor.id,
                "team_id": team.id,
                "description": description,
                "receipt": receipt,
                "points": points,
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['sponsor_id'] == sponsor.id
        assert data['team_id'] == team.id
        assert data['description'] == description
        assert data['receipt'] == receipt
        assert data['points'] == points
        assert isinstance(data['espy_id'], int) is True
        espy_id = data['espy_id']
        assert Espys.query.filter(Espys.id == espy_id).first() is not None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
def test_required_fields_of_espys(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
):
    with mlsb_app.app_context():
        sponsor = sponsor_factory()
        description = random_name("Description")
        receipt = random_name("Receipt")
        points = 100
        response = client.post(
            url_for("rest.espys"),
            json={
                "sponsor_id": sponsor.id,
                "description": description,
                "receipt": receipt,
                "points": points,
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
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('espys_factory')
def test_update_espy(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    espys_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        team = team_factory(
            random_name('Color'),
            sponsor=sponsor,
            league=league
        )
        description = random_name("Description")
        points = 100
        espy = espys_factory(team, sponsor=sponsor, description=description)
        response = client.put(
            url_for("rest.espy", espy_id=espy.id),
            json={
                "points": points
            },
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['points'] == points
        assert data['espy_id'] == espy.id


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('espys_factory')
def test_delete_espy(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    espys_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        team = team_factory(
            random_name('Color'),
            sponsor=sponsor,
            league=league
        )
        description = random_name("Description")
        espy = espys_factory(team, sponsor=sponsor, description=description)
        response = client.delete(
            url_for("rest.espy", espy_id=espy.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        assert Espys.query.filter(Espys.id == espy.id).first() is None


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('admin_header')
def test_get_all_espys(
    mlsb_app,
    client,
    admin_header,
):
    with mlsb_app.app_context():
        response = client.get(
            url_for("rest.espys"),
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
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('espys_factory')
def test_get_espy(
    mlsb_app,
    client,
    admin_header,
    sponsor_factory,
    team_factory,
    league_factory,
    espys_factory
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        team = team_factory(
            random_name('Color'),
            sponsor=sponsor,
            league=league
        )
        description = random_name("Description")
        espy = espys_factory(team, sponsor=sponsor, description=description)
        response = client.get(
            url_for("rest.espy", espy_id=espy.id),
            follow_redirects=True,
            headers=admin_header
        )
        assert response.status_code == 200
        data = loads(response.data)
        assert data['espy_id'] == espy.id
        assert data['points'] == espy.points
