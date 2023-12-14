import json

import pytest

from tests.fixtures import flask_app, client
from webapp.todo_items import delete_all_todo_items


@pytest.fixture(autouse=True)
def clear_database():
    yield

    delete_all_todo_items()


@pytest.mark.usefixtures('flask_app', 'client')
def test_save_and_get_items(client):
    content = 'Test Item #1'

    post_response = post_item(client, content)
    assert post_response.status_code == 200

    get_response, items = get_all_items(client)
    assert get_response.status_code == 200
    assert len(items) == 1
    assert items[0]['content'] == content


def get_all_items(client):
    response = client.get('/api/items')
    if response.status_code == 200:
        return response, json.loads(response.data)
    return response, None


def post_item(client, content):
    return client.post(
        '/api/items',
        data=json.dumps({
            'content': content
        }),
        content_type='application/json'
    )
