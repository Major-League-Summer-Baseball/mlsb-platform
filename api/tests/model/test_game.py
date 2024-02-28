import pytest
from api.errors import DivisionDoesNotExist, InvalidField, \
    LeagueDoesNotExist, TeamDoesNotExist
from api.model import Game, convert_date, Team

INVALID_ENTITY = -1


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", "", ""),
    ("2022-10-01", "10:00", "Rained out", "WP1"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_create_game(
    mlsb_app,
    game_data,
    league_factory,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        Game(
            game_data[0],
            game_data[1],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id,
            status=game_data[2],
            field=game_data[3]
        )


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None),
    (None, None, "Rained out", None),
    (None, None, None, "WP1"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_update_game(
    mlsb_app,
    game_data,
    league_factory,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        game = Game(
            "2016-10-01",
            "9:00",
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id,
            status="",
            field=""
        )
        game.update(
            date=game_data[0],
            time=game_data[1],
            status=game_data[2],
            field=game_data[3]
        )
        if game_data[0] is not None and game_data[1] is not None:
            assert game.date == convert_date(game_data[0], game_data[1])
        if game_data[2] is not None:
            assert game.status == game_data[2]
        if game_data[3] is not None:
            assert game.field == game_data[3]


@pytest.mark.parametrize("invalid_game_data", [
    ("2022-20-01", "10:00", "", ""),
    ("2022-10-01", "30:00", "Rained out", "WP1"),
    ("2022-10-01", "10:00", "Rained out", "NotField"),
    ("2022-10-01", "10:00", 1, "WP1"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_cannot_create_invalid_game(
    mlsb_app,
    invalid_game_data,
    league_factory,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        with pytest.raises(InvalidField):
            Game(
                invalid_game_data[0],
                invalid_game_data[1],
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league_id=league.id,
                division_id=division.id,
                status=invalid_game_data[2],
                field=invalid_game_data[3]
            )


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_game_must_be_in_league(
    mlsb_app,
    game_data,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        with pytest.raises(LeagueDoesNotExist):
            Game(
                game_data[0],
                game_data[1],
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league_id=INVALID_ENTITY,
                division_id=division.id
            )


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_game_update_must_be_in_league(
    mlsb_app,
    game_data,
    division_factory,
    team_factory,
    league_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        game = Game(
            game_data[0],
            game_data[1],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id
        )
        with pytest.raises(LeagueDoesNotExist):
            game.update(league_id=INVALID_ENTITY)


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('team_factory')
def test_game_must_be_in_division(
    mlsb_app,
    game_data,
    league_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        league = league_factory()
        with pytest.raises(DivisionDoesNotExist):
            Game(
                game_data[0],
                game_data[1],
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league_id=league.id,
                division_id=INVALID_ENTITY
            )


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_game_update_must_be_in_division(
    mlsb_app,
    game_data,
    division_factory,
    team_factory,
    league_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        game = Game(
            game_data[0],
            game_data[1],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id
        )
        with pytest.raises(DivisionDoesNotExist):
            game.update(division_id=INVALID_ENTITY)


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('team_factory')
def test_team_exist_for_game(
    mlsb_app,
    game_data,
    league_factory,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        team = team_factory()
        league = league_factory()
        division = division_factory()
        with pytest.raises(TeamDoesNotExist):
            Game(
                game_data[0],
                game_data[1],
                home_team_id=team.id,
                away_team_id=INVALID_ENTITY,
                league_id=league.id,
                division_id=division.id
            )
        with pytest.raises(TeamDoesNotExist):
            Game(
                game_data[0],
                game_data[1],
                home_team_id=INVALID_ENTITY,
                away_team_id=team.id,
                league_id=league.id,
                division_id=division.id
            )


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", None, None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
def test_update_team_exist_for_game(
    mlsb_app,
    game_data,
    division_factory,
    team_factory,
    league_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        game = Game(
            game_data[0],
            game_data[1],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id
        )
        with pytest.raises(TeamDoesNotExist):
            game.update(home_team_id=INVALID_ENTITY)
        with pytest.raises(TeamDoesNotExist):
            game.update(away_team_id=INVALID_ENTITY)


@pytest.mark.parametrize("game_data", [
    ("2022-10-01", "10:00", "", ""),
    ("2022-10-01", "10:00", "Rained out", "WP1"),
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
def test_uncompleted_game_summary(
    mlsb_app,
    game_data,
    league_factory,
    division_factory,
    team_factory
):
    with mlsb_app.app_context():
        home_team = team_factory()
        away_team = team_factory()
        division = division_factory()
        league = league_factory()
        game = Game(
            game_data[0],
            game_data[1],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            league_id=league.id,
            division_id=division.id,
            status=game_data[2],
            field=game_data[3]
        )
        summary = game.summary()
        assert summary['away_score'] == 0
        assert summary['away_bats'] == 0
        assert summary['home_score'] == 0
        assert summary['home_bats'] == 0


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('bat_factory')
def test_completed_game_summary(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory,
    bat_factory
):
    with mlsb_app.app_context():
        # setup players
        home_player = player_factory()
        away_player = player_factory()

        # setup teams
        home_team = team_factory(players=[home_player])
        away_team = team_factory(players=[away_player])

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

        # add some scores
        bat_factory(
            game=game,
            player=home_player,
            team=home_team,
            rbi=1
        )
        bat_factory(
            game=game,
            player=away_player,
            team=away_team
        )
        bat_factory(
            game=game,
            player=away_player,
            team=away_team
        )

        # game was low scoring 1-0
        summary = game.summary()
        assert summary['away_score'] == 0
        assert summary['away_bats'] == 2
        assert summary['home_score'] == 1
        assert summary['home_bats'] == 1


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('bat_factory')
def test_games_with_scores(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory,
    bat_factory
):
    with mlsb_app.app_context():
        # setup players
        home_player = player_factory()
        away_player = player_factory()

        # setup teams
        home_team = team_factory(players=[home_player])
        away_team = team_factory(players=[away_player])

        # setup divion and league
        division = division_factory()
        league = league_factory()

        # create the game
        game_with_score = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )

        # add some scores
        bat_factory(
            game=game_with_score,
            player=home_player,
            team=home_team,
            rbi=0
        )
        team = Team.query.get(home_team.id)
        games = Game.games_with_scores([team])
        assert len(games) > 0
        game_ids = [game.id for game in games]
        assert game_with_score.id in game_ids


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('bat_factory')
def test_games_with_scores_no_submission(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory,
    bat_factory
):
    with mlsb_app.app_context():
        # setup players
        home_player = player_factory()
        away_player = player_factory()

        # setup teams
        home_team = team_factory(players=[home_player])
        away_team = team_factory(players=[away_player])

        # setup divion and league
        division = division_factory()
        league = league_factory()

        # create the game
        game_with_score = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )

        # add some scores
        bat_factory(
            game=game_with_score,
            player=home_player,
            team=home_team,
            rbi=0
        )
        team = Team.query.get(away_team.id)
        games = Game.games_with_scores([team])
        game_ids = [game.id for game in games]
        assert game_with_score.id not in game_ids


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_games_games_needing_scores(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory
):
    with mlsb_app.app_context():
        # setup players
        home_player = player_factory()
        away_player = player_factory()

        # setup teams
        home_team = team_factory(players=[home_player])
        away_team = team_factory(players=[away_player])

        # setup divion and league
        division = division_factory()
        league = league_factory()

        # create the game
        game_with_score = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )

        team = Team.query.get(away_team.id)
        games = Game.games_needing_scores([team])
        game_ids = [game.id for game in games]
        assert len(game_ids) > 0
        assert game_with_score.id in game_ids


@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('game_factory')
@pytest.mark.usefixtures('player_factory')
def test_games_games_needing_scores_already_submitted(
    mlsb_app,
    league_factory,
    division_factory,
    team_factory,
    game_factory,
    player_factory,
    bat_factory
):
    with mlsb_app.app_context():
        # setup players
        home_player = player_factory()
        away_player = player_factory()

        # setup teams
        home_team = team_factory(players=[home_player])
        away_team = team_factory(players=[away_player])

        # setup divion and league
        division = division_factory()
        league = league_factory()

        # create the game
        game_with_score = game_factory(
            home_team=home_team,
            away_team=away_team,
            league=league,
            division=division
        )

        # add some scores
        bat_factory(
            game=game_with_score,
            player=home_player,
            team=home_team,
            rbi=0
        )
        team = Team.query.get(home_team.id)
        games = Game.games_needing_scores([team])
        game_ids = [game.id for game in games]
        assert game_with_score.id not in game_ids
