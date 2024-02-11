import pytest
from api.errors import InvalidField, LeagueEventDoesNotExist, PlayerDoesNotExist, PlayerNotOnTeam
from api.model import LeagueEventDate


@pytest.mark.parametrize("league_event_date_data", [
    ("2022-10-01", "12:01"),
    ("2023-10-01", "1:01")
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
def test_create_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_data
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        LeagueEventDate(
            date=league_event_date_data[0],
            time=league_event_date_data[1],
            league_event_id=league_event.id
        )


@pytest.mark.parametrize("invalid_league_event_date_data", [
    ("2022-10-01", "25:01"),
    ("2023-13-01", "1:01")
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
def test_cannot_create_invalid_league_event_date(
    mlsb_app,
    league_event_factory,
    invalid_league_event_date_data
):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            league_event = league_event_factory("League Event", "Description")
            LeagueEventDate(
                date=invalid_league_event_date_data[0],
                time=invalid_league_event_date_data[1],
                league_event_id=league_event.id
            )


@pytest.mark.parametrize("league_event_date_data", [
    ("2022-10-01", "12:01")
])
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_create_league_event_date_non_existent_event(
    mlsb_app,
    league_event_date_data
):
    with mlsb_app.app_context():
        with pytest.raises(LeagueEventDoesNotExist):
            LeagueEventDate(
                date=league_event_date_data[0],
                time=league_event_date_data[1],
                league_event_id=-1
            )


@pytest.mark.parametrize("league_event_date_data", [
    ("2022-10-01", None),
    (None, "1:01")
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
def test_update_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_data
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        league_event_date = LeagueEventDate(
            date="2022-10-01",
            time="10:00",
            league_event_id=league_event.id
        )
        league_event_date.update(
            date=league_event_date_data[0],
            time=league_event_date_data[1]
        )


@pytest.mark.parametrize("invalid_league_event_date_data", [
    (None, "25:01"),
    ("2023-13-01", None)
])
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('league_event_factory')
def test_cannot_update_invalid_league_event_date(
    mlsb_app,
    league_event_factory,
    invalid_league_event_date_data
):
    with mlsb_app.app_context():
        with pytest.raises(InvalidField):
            league_event = league_event_factory("League Event", "Description")
            league_event_date = LeagueEventDate(
                date="2022-10-01",
                time="10:00",
                league_event_id=league_event.id
            )
            league_event_date.update(
                date=invalid_league_event_date_data[0],
                time=invalid_league_event_date_data[1]
            )


@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_cannot_update_league_event_date_non_existent_event(
    mlsb_app,
    league_event_factory
):
    with mlsb_app.app_context():
        with pytest.raises(LeagueEventDoesNotExist):
            league_event = league_event_factory("League Event", "Description")
            league_event_date = LeagueEventDate(
                date="2022-10-01",
                time="10:00",
                league_event_id=league_event.id
            )
            league_event_date.update(
                league_event_id=-1
            )


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_player_signed_up_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        event_date = league_event_date_factory(league_event)
        player = player_factory()
        assert event_date.signup_player(player.id) is True
        assert event_date.is_player_signed_up(player.id) is True


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_player_not_signed_up_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        event_date = league_event_date_factory(league_event)
        player = player_factory()
        assert event_date.is_player_signed_up(player.id) is False


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_player_cant_sign_up_twice_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        event_date = league_event_date_factory(league_event)
        player = player_factory()
        event_date.signup_player(player.id)
        # they cant sign up twice
        assert event_date.signup_player(player.id) is False


@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_non_existent_player_cant_sign_up_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        event_date = league_event_date_factory(league_event)
        with pytest.raises(PlayerDoesNotExist):
            event_date.signup_player(-1)


@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_non_existent_player_cant_removed_league_event_date(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        event_date = league_event_date_factory(league_event)
        with pytest.raises(PlayerDoesNotExist):
            event_date.remove_player(-1)


@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_can_removed_league_event_date_attendee(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        player = player_factory()
        event_date = league_event_date_factory(league_event, attendees=[player])
        event_date.remove_player(player.id)


@pytest.mark.usefixtures('league_event_date_factory')
@pytest.mark.usefixtures('league_event_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_cant_removed_league_event_date_non_attendee(
    mlsb_app,
    league_event_factory,
    league_event_date_factory,
    player_factory
):
    with mlsb_app.app_context():
        league_event = league_event_factory("League Event", "Description")
        player = player_factory()
        event_date = league_event_date_factory(league_event)
        with pytest.raises(PlayerNotOnTeam):
            # TODO: this error should change to its own name
            event_date.remove_player(player.id)
