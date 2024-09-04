import pytest
from datetime import datetime
from api.importers.league import BACKGROUND, HEADERS, INVALID_TEAM, TEAM_NOT_FOUND, LeagueList


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
def test_able_import_league(
    mlsb_app,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        away_team = team_factory(sponsor=sponsor, league=league)
        date = datetime.today().strftime("%Y-%m-%d")
        time = datetime.today().strftime("%H:%M")
        header_line = ",".join([
            HEADERS["home"],
            HEADERS["away"],
            HEADERS["date"],
            HEADERS["time"],
            HEADERS["field"]]
        )
        entry = "{},{},{},{},{}".format(
            str(home_team), str(away_team), date, time, "WP1"
        )
        lines = [
            "{}:,{},".format(BACKGROUND['league'], str(league)),
            "{}:,{},".format(
                BACKGROUND['division'],
                str(division)
            ),
            header_line,
            entry
        ]
        league_importer = LeagueList(lines)
        league_importer.import_league_functional()
        assert len(league_importer.warnings) == 0


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('team_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('division_factory')
@pytest.mark.usefixtures('player_factory')
def test_able_import_league_with_warnings(
    mlsb_app,
    sponsor_factory,
    team_factory,
    league_factory,
    division_factory,
    player_factory
):
    with mlsb_app.app_context():
        player = player_factory()
        division = division_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        home_team = team_factory(
            sponsor=sponsor, league=league, players=[player]
        )
        date = datetime.today().strftime("%Y-%m-%d")
        time = datetime.today().strftime("%H:%M")
        header_line = ",".join([
            HEADERS["home"],
            HEADERS["away"],
            HEADERS["date"],
            HEADERS["time"],
            HEADERS["field"]]
        )
        not_a_team = "not a team"
        entry = "{},{},{},{},{}".format(
            str(home_team), not_a_team, date, time, "WP1"
        )
        lines = [
            "{}:,{},".format(BACKGROUND['league'], str(league)),
            "{}:,{},".format(
                BACKGROUND['division'],
                str(division)
            ),
            header_line,
            entry
        ]
        league_importer = LeagueList(lines)
        league_importer.import_league_functional()
        assert len(league_importer.warnings) == 1
        assert "Did not find team" in league_importer.warnings[0]
        assert INVALID_TEAM.format(not_a_team) in league_importer.warnings[0]