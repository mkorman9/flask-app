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

    post_response, _ = post_item(client, content)
    assert post_response.status_code == 200

    get_response, items = get_all_items(client)
    assert get_response.status_code == 200
    assert len(items) == 1
    assert items[0]['content'] == content


@pytest.mark.usefixtures('flask_app', 'client')
def test_save_and_delete_item(client):
    post_response, item_id = post_item(client, 'Test Item #2')
    assert post_response.status_code == 200

    delete_response, _ = delete_item(client, item_id)
    assert delete_response.status_code == 200

    get_response, items = get_all_items(client)
    assert get_response.status_code == 200
    assert len(items) == 0


@pytest.mark.usefixtures('flask_app', 'client')
def test_delete_non_existing_item(client):
    delete_response, message = delete_item(client, 'non-existing')
    assert delete_response.status_code == 404
    assert message['type'] == 'ItemNotFound'


@pytest.mark.usefixtures('flask_app', 'client')
def test_update_item(client):
    post_response, item_id = post_item(client, 'Test Item #3')
    assert post_response.status_code == 200

    updated_content = 'Updated Item'
    put_response, _ = update_item(client, item_id, updated_content)
    assert put_response.status_code == 200

    get_response, items = get_all_items(client)
    assert get_response.status_code == 200
    assert len(items) == 1
    assert items[0]['content'] == updated_content


@pytest.mark.usefixtures('flask_app', 'client')
def test_update_non_existing_item(client):
    put_response, message = update_item(client, 'non-existing', 'Content')
    assert put_response.status_code == 404
    assert message['type'] == 'ItemNotFound'


def get_all_items(client):
    response = client.get('/api/items')
    if response.status_code == 200:
        return response, json.loads(response.data)
    return response, None


def post_item(client, content):
    response = client.post(
        '/api/items',
        data=json.dumps({
            'content': content
        }),
        content_type='application/json'
    )
    if response.status_code == 200:
        return response, json.loads(response.data)['id']
    return response, None


def update_item(client, item_id, content):
    response = client.put(
        f'/api/items/{item_id}',
        data=json.dumps({
            'content': content
        }),
        content_type='application/json'
    )
    return response, json.loads(response.data)


def delete_item(client, item_id):
    response = client.delete(f'/api/items/{item_id}')
    return response, json.loads(response.data)
