import pytest

from webapp.app import app


@pytest.fixture()
def flask_app():
    app.config.update({'TESTING': True})
    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def runner(flask_app):
    return flask_app.test_cli_runner()
