import pytest
from api.app import create_app
from api.extensions import DB
from api.model import Sponsor, Player


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
def sponsor_factory(sponsor_name, link=None, description=None):
    sponsor = Sponsor(sponsor_name, link=link, description=description)
    DB.session.add(sponsor)
    DB.session.commit()
    return sponsor


@factory_fixture
def player_factory(name, email, gender, password="default", active=True):
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
