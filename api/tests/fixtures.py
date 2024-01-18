import pytest
import uuid
from api.app import create_app
from api.extensions import DB
from api.model import Sponsor, Player, LeagueEvent, LeagueEventDate


@pytest.fixture(scope="session")
def mlsb_app():
    """The mlsb flask app."""
    mlsb_app = create_app()
    mlsb_app.config.update({
        "SERVER_NAME": 'localhost:5000',
    })

    # other setups
    yield mlsb_app

    # clean up / reset resources
    pass


@pytest.fixture(scope="session")
def client(mlsb_app):
    return mlsb_app.test_client()


@pytest.fixture(scope="session")
def runner(mlsb_app):
    return mlsb_app.test_cli_runner()


def factory_fixture(factory):
    @pytest.fixture(scope='session')
    def maker():
        return factory
    maker.__name__ = factory.__name__
    return maker


@factory_fixture
def sponsor_factory(sponsor_name: str = '', link=None, description=None):
    sponsor_name = sponsor_name if sponsor_name != '' else f"Sponsor - {str(uuid.uuid4())}"
    sponsor = Sponsor(sponsor_name, link=link, description=description)
    DB.session.add(sponsor)
    DB.session.commit()
    return sponsor


@factory_fixture
def player_factory(name: str = '', email: str = '', gender="M", password="default", active=True):
    name = name if name != '' else f"{str(uuid.uuid4())}"
    email = email if email != '' else f"{str(uuid.uuid4())}@mlsb.ca"
    player = Player(
        name=name,
        email=email,
        gender=gender,
        password=password,
        active=active
    )
    DB.session.add(player)
    DB.session.commit()
    return player


@factory_fixture
def league_event_factory(
    name: str = '',
    description: str = 'Description',
    active: bool = True
) -> LeagueEvent:
    name = name if name != '' else f"Event - {str(uuid.uuid4())}"
    league_event = LeagueEvent(
        name=name,
        description=description,
        active=active,
    )
    DB.session.add(league_event)
    DB.session.commit()
    return league_event


@factory_fixture
def league_event_date_factory(
    league_event: LeagueEvent,
    date: str = "2022-10-01",
    time: str = "10:00",
    attendees: list[Player] = []
) -> LeagueEventDate:
    league_event_date = LeagueEventDate(
        date=date,
        time=time,
        league_event_id=league_event.id,
    )
    for player in attendees:
        league_event_date.signup_player(player.id)
    DB.session.add(league_event)
    DB.session.commit()
    return league_event_date
