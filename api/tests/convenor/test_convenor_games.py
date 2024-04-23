from datetime import datetime
from api.model import Bat, split_datetime, Game
from flask import url_for
import io
import pytest


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
def test_convenor_new_game_page(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory
):
    """Test convenor can view games."""
    with mlsb_app.app_context():
        league = league_factory()
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.new_game_page", league_id=league.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_edit_game_page(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    game_factory
):
    """Test convenor can view games."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game = game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.edit_game_page", game_id=game.id),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_games_page(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    game_factory
):
    """Test convenor can view games."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.games_page"), follow_redirects=True
        )
        assert response.status_code == 200
        assert str(home_team) in str(response.data)
        assert str(away_team) in str(response.data)
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_games_filter_team_page(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    game_factory
):
    """Test convenor can view games by team."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        other_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game_factory(
            other_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.games_page", team_id=home_team.id),
            follow_redirects=True,
        )
        assert response.status_code == 200
        games_container = get_games_container(str(response.data))
        assert str(home_team) in games_container
        assert str(away_team) in games_container
        assert str(other_team) not in games_container
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_convenor_submit_new_games(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory
):
    """Test convenors can create game."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_game"),
            follow_redirects=True,
            data={
                'home_team_id': home_team.id,
                'away_team_id': away_team.id,
                'league_id': league.id,
                'division_id': division.id,
                'date': game_date,
                'time': game_time,
                'status': 'some-status',
                'field': 'WP1'
            }
        )
        assert response.status_code == 200
        game_header = get_game_header(str(response.data))
        assert str(home_team) in game_header
        assert str(away_team) in game_header
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_update_new_games(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    game_factory
):
    """Test convenors can update game."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game = game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_game"),
            follow_redirects=True,
            data={
                'home_team_id': home_team.id,
                'away_team_id': away_team.id,
                'league_id': league.id,
                'division_id': division.id,
                'date': game_date,
                'time': game_time,
                'status': 'some-status',
                'field': 'WP1',
                'game_id': game.id
            }
        )
        assert response.status_code == 200
        game_header = get_game_header(str(response.data))
        assert str(home_team) in game_header
        assert str(away_team) in game_header
        assert not url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_submit_bat(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    player_factory,
    game_factory
):
    """Test convenor can submit a bat."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game = game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        player = player_factory()
        auth.login(convenor.email)
        response = client.post(
            url_for(
                "convenor.submit_bat", team_id=home_team.id, game_id=game.id
            ),
            follow_redirects=True,
            data={
                'player_id': player.id,
                'rbi': 0,
                'inning': 1,
                'hit': 's'
            }
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        bat_exist = Bat.query.filter(Bat.game_id == game.id).all()
        assert len(bat_exist) > 0


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('bat_factory')
def test_convenor_delete_bat(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
    player_factory,
    game_factory,
    bat_factory
):
    """Test convenor can delete a bat."""
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        game = game_factory(
            home_team,
            away_team,
            league,
            division,
            date=game_date,
            time=game_time
        )
        player = player_factory()
        bat = bat_factory(game, player, home_team,)
        auth.login(convenor.email)
        response = client.delete(
            url_for("convenor.delete_bat", bat_id=bat.id, game_id=game.id),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        bat_exist = Bat.query.get(bat.id)
        assert bat_exist is None


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
def test_convenor_download_game_template(mlsb_app, client, auth, convenor):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        auth.login(convenor.email)
        response = client.get(
            url_for("convenor.game_template"),
            follow_redirects=True
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        assert "Ex. MLSB" in str(response.data)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('convenor')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
def test_convenor_submit_game_template(
    mlsb_app,
    client,
    auth,
    convenor,
    league_factory,
    division_factory,
    team_factory,
):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        league = league_factory()
        home_team = team_factory(league=league)
        away_team = team_factory(league=league)
        division = division_factory()
        game_date, game_time = split_datetime(datetime.today())
        template = f"""League,{league.name},,,
Division,{division.name},,,
Home Team, Away Team,Date,Time,Field
{home_team},{away_team},{game_date},{game_time},WP1
        """
        data = {
            "file": (io.BytesIO(str.encode(template)), 'gameTemplate.csv')
        }
        auth.login(convenor.email)
        response = client.post(
            url_for("convenor.submit_game_template"),
            follow_redirects=True,
            data=data,
            content_type='multipart/form-data'
        )
        assert not url_for("website.loginpage").endswith(response.request.path)
        assert response.status_code == 200
        games = Game.query.filter(Game.league_id == league.id).all()
        assert len(games) > 0


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_delete_bat(mlsb_app, client, auth):
    """Test only convenor can delete a bat."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.delete(
            url_for("convenor.delete_bat", bat_id=1, game_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_bat(mlsb_app, client, auth):
    """Test only convenor can submit a bat."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.submit_bat", team_id=1, game_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_games_page(mlsb_app, client, auth):
    """Test only convenors can view/edit games."""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.games_page"),
            follow_redirects=True,
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_game(mlsb_app, client, auth):
    """Test convenors can create game."""
    with mlsb_app.app_context():
        auth.logout()
        game_date, game_time = split_datetime(datetime.today())
        response = client.post(
            url_for("convenor.submit_game"),
            follow_redirects=True,
            data={
                'home_team_id': 1,
                'away_team_id': 2,
                'league_id': 1,
                'division_id': 1,
                'date': game_date,
                'time': game_time,
                'status': 'some-status',
                'field': 'WP1'
            }
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_game_template(mlsb_app, client, auth):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.game_template"),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_submit_game_template(mlsb_app, client, auth):
    """Test only convenor can download the games template"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.submit_game_template"),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_new_game_page(mlsb_app, client, auth):
    """Test only convenor view new game page"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.get(
            url_for("convenor.new_game_page", league_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


@pytest.mark.convenor
@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
def test_only_convenor_edit_game_page(mlsb_app, client, auth):
    """Test only convenor can view edit game page"""
    with mlsb_app.app_context():
        auth.logout()
        response = client.post(
            url_for("convenor.edit_game_page", game_id=1),
            follow_redirects=True
        )
        assert url_for("website.loginpage").endswith(response.request.path)


def get_games_container(response) -> str:
    """Get the games container from response."""
    return response.split('"games-container')[1]


def get_game_header(response) -> str:
    """Get the game header from response."""
    return response.split('</h1>')[0]
