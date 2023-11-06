import pytest
from api.app import create_app


@pytest.fixture()
def mlsb_app():
    """The mlsb flask app."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setups

    yield app

    # clean up / reset resources
    pass


@pytest.fixture()
def client(mlsb_app):
    return mlsb_app.test_client()


@pytest.fixture()
def runner(mlsb_app):
    return mlsb_app.test_cli_runner()
