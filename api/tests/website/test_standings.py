import pytest
from datetime import date
from api.model import League
from flask import url_for
from api.helper import loads

THIS_YEAR = date.today().year


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_espys_breakdown_request(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for("website.espys_breakdown_request", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        response_data = loads(response.data)
        assert response_data['name'] == "ESPYS Breakdown"
        assert isinstance(response_data['children'], list) is True


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_all_time_leaders_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for("website.all_time_leaders_page", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_leaders_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for("website.leaders_page", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_stats_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for("website.stats_page", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_standings_page(mlsb_app, client):
    with mlsb_app.app_context():
        league = League.query.first()
        url = url_for(
            "website.standings", league_id=league.id, year=THIS_YEAR
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
