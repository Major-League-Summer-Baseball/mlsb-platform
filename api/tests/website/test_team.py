import pytest
from datetime import date
from flask import url_for
from api.helper import loads
from api.model import Team, Player


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
        team = Team.query.filter(Team.sponsor_name.is_not(None)).first()
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
        Team.query.filter(Team.sponsor_name.is_not(None)).first()
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
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_page_captain(
    mlsb_app,
    client,
    team_factory,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        teammate = player_factory()
        player = player_factory()
        team = team_factory(players=[teammate], captain=player)
        auth.login(player.email)
        url = url_for(
            "website.team_page",
            year=THIS_YEAR,
            team_id=team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        # email should be visible
        assert teammate.email in data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_player_page(mlsb_app, client):
    with mlsb_app.app_context():
        player = Player.query.first()
        url = url_for(
            "website.player_page",
            year=THIS_YEAR,
            player_id=player.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
def test_nonexistent_player_page(mlsb_app, client):
    with mlsb_app.app_context():
        url = url_for(
            "website.player_page",
            year=THIS_YEAR,
            player_id=INVALID_ENTITY
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        assert "<title>Player not found</title>" in data


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_request_to_join_team(
    mlsb_app,
    client,
    team_factory,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        new_player = player_factory()
        team = team_factory()
        auth.login(new_player.email)
        url = url_for(
            "website.request_to_join_team",
            team_id=team.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        join_request = loads(response.data)
        assert join_request['team']['team_id'] == team.id
        assert join_request['email'] == new_player.email


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('team_factory')
def test_request_to_join_team_not_signed_in(
    mlsb_app,
    client,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        auth.logout()
        team = team_factory()
        url = url_for(
            "website.request_to_join_team",
            team_id=team.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 401


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_request_to_join_nonexistent_team(
    mlsb_app,
    client,
    player_factory,
    auth
):
    with mlsb_app.app_context():
        new_player = player_factory()
        auth.login(new_player.email)
        url = url_for(
            "website.request_to_join_team",
            team_id=INVALID_ENTITY
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_remove_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team = team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=team.id,
            player_id=teammate.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        remove_request = loads(response.data)
        assert remove_request == teammate.id


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_nonexistent_team_remove_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=INVALID_ENTITY,
            player_id=teammate.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_remove_nonexistent_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_remove_player",
            team_id=team.id,
            player_id=INVALID_ENTITY
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        new_player = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player",
            team_id=team.id,
            player_id=new_player.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 200
        assert loads(response.data) == new_player.id


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_player_already_on_team(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        teammate = player_factory()
        team = team_factory(players=[teammate], captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player",
            team_id=team.id,
            player_id=teammate.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404
        assert loads(response.data) == "Player already on team"


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_team_add_nonexistent_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player",
            team_id=team.id,
            player_id=INVALID_ENTITY
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404
        assert loads(response.data)['details'] == INVALID_ENTITY


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_nonexistent_team_add_player(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        new_player = player_factory()
        team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.team_add_player",
            team_id=INVALID_ENTITY,
            player_id=new_player.id
        )
        response = client.post(url, follow_redirects=True)
        assert response.status_code == 404
        assert response.data.decode("utf-8") == "Team does not exist"


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_accept_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request",
            team_id=team.id,
            request_id=request.id
        )
        response = client.post(
            url,
            json={"accept": True},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert loads(response.data) is True


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_reject_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request",
            team_id=team.id,
            request_id=request.id
        )
        response = client.post(
            url,
            json={"accept": False},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert loads(response.data) is True


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_not_captain_cannot_respond_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        player = player_factory()
        team = team_factory(players=[player])
        request = join_league_request_factory(team)
        auth.login(player.email)
        url = url_for(
            "website.captain_respond_league_request",
            team_id=team.id,
            request_id=request.id
        )
        response = client.post(
            url,
            json={"accept": False},
            follow_redirects=True
        )
        assert response.status_code == 403


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('auth')
def test_captain_cannot_respond_nonexistent_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request",
            team_id=team.id,
            request_id=INVALID_ENTITY
        )
        response = client.post(
            url,
            json={"accept": True},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert loads(response.data) is False


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('join_league_request_factory')
@pytest.mark.usefixtures('auth')
def test_captain_cannot_rerespond_team_request(
    mlsb_app,
    client,
    player_factory,
    team_factory,
    join_league_request_factory,
    auth
):
    with mlsb_app.app_context():
        captain = player_factory()
        team = team_factory(captain=captain)
        request = join_league_request_factory(team)
        auth.login(captain.email)
        url = url_for(
            "website.captain_respond_league_request",
            team_id=team.id,
            request_id=request.id
        )
        response = client.post(
            url,
            json={"accept": True},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert loads(response.data) is True

        response = client.post(
            url,
            json={"accept": True},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert loads(response.data) is False
