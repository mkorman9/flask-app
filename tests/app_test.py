import pytest

from tests.fixtures import flask_app, client


@pytest.mark.usefixtures('flask_app', 'client')
def test_get_items(client):
    response = client.get('/api/items')
    assert response.status_code == 200
