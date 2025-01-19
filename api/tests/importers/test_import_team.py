import uuid
import pytest
from api.importers.team import BACKGROUND, HEADERS, TeamList
from api.models.team import Team


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
def test_able_import_team(
    mlsb_app,
    sponsor_factory,
    league_factory,
):
    with mlsb_app.app_context():
        league = league_factory()
        sponsor = sponsor_factory()
        captain_name = random_name('captain')
        captain_email = random_email()
        lines = [
            "{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
            "{}:,{},".format(BACKGROUND['team_color'], random_name('color')),
            "{}:,{},".format(BACKGROUND['captain_name'], captain_name),
            "{}:,{},".format(BACKGROUND['league_name'], league),
            "{},{},{}".format(
                HEADERS['name'], HEADERS['email'], HEADERS['gender']
            ),
            "{},{},{}".format(captain_name, captain_email, "M"),
            "{},{},{}".format(random_name('player'), random_email(), "M"),
            "{},{},{}".format(random_name('player'), random_email(), "F")
        ]
        # import the a test team
        importer = TeamList(lines)
        importer.add_team_functional()
        assert len(importer.warnings) == 0
        teams = (
            Team.query
            .filter(Team.sponsor_id == sponsor.id)
        ).all()
        assert len(teams) == 1, "Import team was not created"
        assert len(teams[0].players) == 3, "Imported players not added to team"


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('player_factory')
def test_able_import_team_player_already_exists(
    mlsb_app,
    sponsor_factory,
    league_factory,
    player_factory
):
    with mlsb_app.app_context():
        captain = player_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        captain_name = str(captain)
        captain_email = captain.email
        lines = [
            "{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
            "{}:,{},".format(BACKGROUND['team_color'], random_name('color')),
            "{}:,{},".format(BACKGROUND['captain_name'], captain_name),
            "{}:,{},".format(BACKGROUND['league_name'], league),
            "{},{},{}".format(
                HEADERS['name'], HEADERS['email'], HEADERS['gender']
            ),
            "{},{},{}".format(captain_name, captain_email, "M"),
            "{},{},{}".format(random_name('player'), random_email(), "M")
        ]
        # import the a test team
        importer = TeamList(lines)
        importer.add_team_functional()
        assert len(importer.warnings) == 0
        teams = (
            Team.query
            .filter(Team.sponsor_id == sponsor.id)
        ).all()
        assert len(teams) == 1, "Import team was not created"
        assert len(teams[0].players) == 2, "Imported players not added to team"
        assert captain.id in [p.id for p in teams[0].players], "Did not re-use existing player"


@pytest.mark.rest
@pytest.mark.usefixtures('mlsb_app')
@pytest.mark.usefixtures('sponsor_factory')
@pytest.mark.usefixtures('league_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('team_factory')
def test_able_import_players_onto_existing_team(
    mlsb_app,
    sponsor_factory,
    league_factory,
    player_factory,
    team_factory
):
    with mlsb_app.app_context():
        captain = player_factory()
        league = league_factory()
        sponsor = sponsor_factory()
        color = random_name('color')
        team = team_factory(color, sponsor=sponsor, league=league)
        captain_name = str(captain)
        captain_email = captain.email
        lines = [
            "{}:,{},".format(BACKGROUND['sponsor_name'], sponsor),
            "{}:,{},".format(BACKGROUND['team_color'], color),
            "{}:,{},".format(BACKGROUND['captain_name'], captain_name),
            "{}:,{},".format(BACKGROUND['league_name'], league),
            "{},{},{}".format(
                HEADERS['name'], HEADERS['email'], HEADERS['gender']
            ),
            "{},{},{}".format(captain_name, captain_email, "M"),
            "{},{},{}".format(random_name('player'), random_email(), "M")
        ]
        # import the a test team
        importer = TeamList(lines)
        importer.add_team_functional()
        assert len(importer.warnings) == 0
        updated_team = Team.query.get(team.id)
        assert len(updated_team.players) == 2, "Players not added to existing team"


def random_email() -> str:
    return f"{str(uuid.uuid4())}@mlsb.ca"


def random_name(category: str) -> str:
    return f"{category} - {str(uuid.uuid4())}"
