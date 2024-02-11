import pytest
from datetime import date
from flask import url_for
from api.helper import loads
from api.model import League

THIS_YEAR = date.today().year
INVALID_ENTITY = 100000000


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_schedule_league(mlsb_app, client):
    with mlsb_app.app_context():
        league = League.query.first()
        url = url_for(
            "website.schedule",
            year=THIS_YEAR,
            league_id=league.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_schedule_nonexistent_league(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.schedule",
            year=THIS_YEAR,
            league_id=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        response_data = response.data.decode("utf-8")
        assert "<title>League not found</title>" in response_data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_schedule_cache(mlsb_app, client):
    with mlsb_app.app_context():
        league = League.query.first()
        url = url_for(
            "website.cache_schedule_page",
            year=THIS_YEAR,
            league_id=league.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = loads(response.data)
        assert isinstance(data["items"], list) is True
