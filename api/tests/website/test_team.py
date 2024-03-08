import pytest
import uuid
from datetime import date
from flask import url_for
from api.helper import loads
from api.model import JoinLeagueRequest, Team, Player


THIS_YEAR = date.today().year
INVALID_ENTITY = 100000000


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_team_picture(mlsb_app, client):
    with mlsb_app.app_context():
        team = Team.query.first()
        url = url_for(
            "website.team_picture",
            team=team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_team_picture(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.team_picture",
            team=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_team_picture_by_name(mlsb_app, client):
    with mlsb_app.app_context():
        team = Team.query.filter(Team.sponsor_name.isnot(None)).first()
        url = url_for(
            "website.team_picture",
            team=team.sponsor_name
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_team_picture_by_name(mlsb_app, client):
    with mlsb_app.app_context():
        Team.query.filter(Team.sponsor_name.isnot(None)).first()
        url = url_for(
            "website.team_picture",
            team="DefinitelyNotTeamForSure"
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_team_page(mlsb_app, client):
    with mlsb_app.app_context():
        team = Team.query.filter(Team.year == THIS_YEAR).first()
        url = url_for(
            "website.team_page",
            year=THIS_YEAR,
            team_id=team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_team_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.team_page",
            year=THIS_YEAR,
            team_id=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
def test_join_team_request(client, mlsb_app, team_factory):
    with mlsb_app.app_context():
        team = team_factory()
        url = url_for(
            "website.join_team_request",
            team_id=team.id,
        )
        name = f"player-{str(uuid.uuid4())}"
        email = f"{name}@mlsb.ca"
        response = client.post(
            url,
            data={
                'is_female': False,
                "name": name,
                "email": email
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        result = JoinLeagueRequest.find_request(email)
        assert result is not None
        assert result.email == email


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_join_nonexistent_team_request(client, mlsb_app):
    with mlsb_app.app_context():
        url = url_for(
            "website.join_team_request",
            team_id=INVALID_ENTITY,
        )
        name = f"player-{str(uuid.uuid4())}"
        email = f"{name}@mlsb.ca"
        response = client.post(
            url,
            data={
                'is_female': False,
                "name": name,
                "email": email
            },
            follow_redirects=True
        )
        assert response.status_code == 404
        result = JoinLeagueRequest.find_request(email)
        assert result is None


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('join_league_request_factory')
def test_join_team_duplicated_request(
    client, mlsb_app, team_factory, join_league_request_factory
):
    with mlsb_app.app_context():
        team = team_factory()
        original_request = join_league_request_factory(team)
        url = url_for(
            "website.join_team_request",
            team_id=team.id,
        )
        name = f"player-{str(uuid.uuid4())}"
        response = client.post(
            url,
            data={
                'is_female': False,
                "name": name,
                "email": original_request.email
            },
            follow_redirects=True
        )
        assert response.status_code == 400
        result = JoinLeagueRequest.find_request(original_request.email)
        assert result.name == original_request.name