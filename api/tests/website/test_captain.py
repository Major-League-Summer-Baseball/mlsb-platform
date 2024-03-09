import pytest
from datetime import date
from api.model import Game
from flask import url_for

THIS_YEAR = date.today().year
NON_EXISTENT = 99999999


def create_game(
    player_factory, team_factory, game_factory, division_factory, league_factory
):
    # setup players
    captain = player_factory()

    # setup teams
    home_team = team_factory(players=[captain], captain=captain)
    away_team = team_factory()

    # setup divion and league
    division = division_factory()
    league = league_factory()

    # create the game
    game = game_factory(
        home_team=home_team,
        away_team=away_team,
        league=league,
        division=division
    )
    return (game, captain, home_team)


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_games(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, _) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for("website.captain_games", year=THIS_YEAR)
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        html_response = str(response.data)
        assert "Pending Games" in html_response
        assert str(game.home_team) in html_response
        assert str(game.away_team) in html_response


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('bat_factory')
def test_captain_remove_submitted_score(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory,
        bat_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, home_team) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # add some scores
        bat_factory(
            game=game,
            player=captain,
            team=home_team,
            rbi=0
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_remove_submitted_score",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=home_team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        html_response = str(response.data)

        assert "Pending Games" in html_response
        assert str(game.home_team) in html_response
        assert str(game.away_team) in html_response

        game = Game.query.get(game.id)
        assert len(game.get_team_bats(home_team.id)) == 0


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_score_app_game(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, home_team) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_score_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=home_team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        html_response = str(response.data)

        assert "Submit" in html_response
        assert 'id="submitScoreApp"' in html_response
        assert str(game.home_team) in html_response
        assert str(game.away_team) in html_response


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_score_app_nonexistent_game(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (_, captain, home_team) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_score_app_game",
            year=THIS_YEAR,
            game_id=NON_EXISTENT,
            team_id=home_team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_score_app_nonexistent_team(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, _) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_score_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=NON_EXISTENT
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_score_app_cant_submit_not_captain(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, _) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_score_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=game.away_team_id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 401


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_batting_app_game(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, home_team) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_batting_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=home_team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 200
        html_response = str(response.data)

        assert "Submit game" in html_response
        assert 'id="battingScoreApp"' in html_response
        assert str(game.home_team) in html_response
        assert str(game.away_team) in html_response


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_batting_app_nonexistent_game(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (_, captain, home_team) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_batting_app_game",
            year=THIS_YEAR,
            game_id=NON_EXISTENT,
            team_id=home_team.id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_batting_app_nonexistent_team(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, _) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_batting_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=NON_EXISTENT
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 404


@pytest.mark.usefixtures('client')
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('auth')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
def test_captain_batting_app_cant_submit_not_captain(
        mlsb_app,
        client,
        auth,
        player_factory,
        team_factory,
        game_factory,
        division_factory,
        league_factory
):
    with mlsb_app.app_context():
        # setup game
        (game, captain, _) = create_game(
            player_factory,
            team_factory,
            game_factory,
            division_factory,
            league_factory
        )

        # login as some captain
        auth.login(captain.email)
        url = url_for(
            "website.captain_batting_app_game",
            year=THIS_YEAR,
            game_id=game.id,
            team_id=game.away_team_id
        )
        response = client.get(url, follow_redirects=True)
        assert response.status_code == 401
