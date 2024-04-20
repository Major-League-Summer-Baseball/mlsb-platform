from datetime import datetime, date
from api.model import split_datetime, Team
from flask import url_for
import io
import pytest


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_create_team(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    sponsor_factory
):
    """Test convenor able to add team."""
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = "Pink"
        year = date.today().year
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_team"),
            follow_redirects=True,
            data={
                'league_id': league.id,
                'sponsor_id': sponsor.id,
                'year': year,
                'color': "Pink"
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        teams = Team.query.filter(Team.league_id == league.id).all()
        assert len(teams) > 0
        team = teams[0]
        assert team.color == color
        assert team.sponsor_id == sponsor.id
        assert team.year == year


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
def test_convenor_update_team(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    sponsor_factory,
    team_factory
):
    """Test convenor able to add team."""
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        color = "Pink"
        year = date.today().year
        auth.login(convenor.email)
        team = team_factory()
        response = client.post(
            url_for("convenor.submit_team"),
            follow_redirects=True,
            data={
                'league_id': league.id,
                'sponsor_id': sponsor.id,
                'year': year,
                'color': "Pink",
                'team_id': team.id
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        teams = Team.query.filter(Team.league_id == league.id).all()
        assert len(teams) > 0
        team = teams[0]
        assert team.color == color
        assert team.sponsor_id == sponsor.id
        assert team.year == year


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_convenor_add_team_player(
    mlsb_app,
    client,
    auth,
    convenor,
    player_factory,
    team_factory
):
    """Test convenor able to add player to team."""
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.add_player_team",
                team_id=team.id,
                player_id=player.id,
                captain=0
            ),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_team = Team.query.get(team.id)
        assert updated_team is not None
        assert len(updated_team.players) > 0
        assert updated_team.player_id is None


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_convenor_add_team_captain(
    mlsb_app,
    client,
    auth,
    convenor,
    player_factory,
    team_factory
):
    """Test convenor able to add captain to team."""
    with mlsb_app.app_context():
        team = team_factory()
        player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.add_player_team",
                team_id=team.id,
                player_id=player.id,
                captain=1
            ),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_team = Team.query.get(team.id)
        assert updated_team is not None
        assert len(updated_team.players) > 0
        assert updated_team.player_id == player.id


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_convenor_remove_team_captain(
    mlsb_app,
    client,
    auth,
    convenor,
    player_factory,
    team_factory
):
    """Test convenor able to remove player from team."""
    with mlsb_app.app_context():
        player = player_factory()
        team = team_factory(players=[player])
        auth.login(convenor.email)
        response = client.delete(
            url_for(
                "convenor.remove_player_team",
                team_id=team.id,
                player_id=player.id,
            ),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        updated_team = Team.query.get(team.id)
        assert updated_team is not None
        assert len(updated_team.players) == 0


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_download_team_template(mlsb_app, client, auth, convenor):
    """Test convenor can download the games template"""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.team_template"),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        assert "Ex. SportZone" in str(response.data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('player_factory')
def test_convenor_submit_team_template(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    sponsor_factory,
    player_factory
):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        captain = player_factory()
        some_player = player_factory()
        color = "Pink"
        template = f"""Sponsor:,{sponsor.name},
Color:,{color},
Captain:,{captain.name},
League:,{league.name},
Player Name,Player Email,Gender (M/F)
{captain.name},{captain.email},{captain.gender}
{some_player.name},{some_player.email},{some_player.gender}
        """
        data = {
            "file": (io.BytesIO(str.encode(template)), 'teamTemplate.csv')
        }
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_team_template"),
            follow_redirects=True,
            data=data,
            content_type='multipart/form-data'
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        teams = Team.query.filter(Team.league_id == league.id).all()
        assert len(teams) > 0
        team = teams[0]
        assert team.color == color
        assert team.sponsor_id == sponsor.id
        assert len(team.players) == 2


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('sponsor_factory')
def test_convenor_add_team_epsy(
    mlsb_app,
    client,
    auth,
    convenor,
    team_factory,
    sponsor_factory
):
    """Test convenor able to remove espy from team"""
    with mlsb_app.app_context():
        team = team_factory()
        sponsor = sponsor_factory()
        description = "some description"
        points = 1.1
        receipt = "BARCODE"
        date, time = split_datetime(datetime.today())
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.add_team_espy", team_id=team.id
            ),
            follow_redirects=True,
            data={
                'sponsor_id': sponsor.id,
                'description': description,
                'points': points,
                'receipt': receipt,
                'time': time,
                'date': date
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        assert "Espy added to team" in str(response.data)
        updated_team = Team.query.get(team.id)
        assert updated_team.espys_total == points
        espy = updated_team.espys[0]
        assert espy.receipt == receipt
        assert espy.description == description
        assert espy.sponsor_id == sponsor.id


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('espys_factory')
def test_convenor_remove_team_epsy(
    mlsb_app,
    client,
    auth,
    convenor,
    team_factory,
    espys_factory
):
    """Test convenor able to remove espy from team"""
    with mlsb_app.app_context():
        team = team_factory()
        espy = espys_factory(team, points=10)
        auth.login(convenor.email)
        response = client.delete(
            url_for(
                "convenor.remove_team_espy", team_id=team.id, espy_id=espy.id
            ),
            follow_redirects=True,
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        updated_team = Team.query.get(team.id)
        assert updated_team.espys_total is None or updated_team.espys_total == 0


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_teams_page(mlsb_app, client, auth):
    """Test only convenor view teams page"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.teams_page"),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_team(mlsb_app, client, auth):
    """Test only convenor submit team"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for(
                "convenor.submit_team",
                team_id=1,
                player_id=1,
                captain=1,
                change=1
            ),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_add_team_player(mlsb_app, client, auth):
    """Test only convenor add team player"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for(
                "convenor.add_player_team",
                team_id=1,
                player_id=1,
                captain=1,
                change=1
            ),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_remove_team_player(mlsb_app, client, auth):
    """Test only convenor remove team player"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.delete(
            url_for(
                "convenor.remove_player_team",
                team_id=1,
                player_id=1,
                captain=1,
                change=1
            ),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_edit_team_page(mlsb_app, client, auth):
    """Test only convenor view edit team page"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for(
                "convenor.edit_team_page",
                team_id=1
            ),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_team_template(mlsb_app, client, auth):
    """Test only convenor can download the team template"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.team_template"),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_team_template(mlsb_app, client, auth):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.submit_team_template"),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_add_team_espy(mlsb_app, client, auth):
    """Test only convenor can add espy to team"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.add_team_espy", team_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_remove_team_espy(mlsb_app, client, auth):
    """Test only convenor can remove espy from team"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.delete(
            url_for("convenor.remove_team_espy", team_id=1, espy_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)
