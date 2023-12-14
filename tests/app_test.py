import json

import pytest

from tests.fixtures import flask_app, client


@pytest.mark.usefixtures('flask_app', 'client')
def test_save_and_get_items(client):
    content = 'Test Item #1'

    post_response = client.post(
        '/api/items',
        data=json.dumps({
            'content': content
        }),
        content_type='application/json'
    )
    assert post_response.status_code == 200

    response = client.get('/api/items')
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body) == 1
    assert body[0]['content'] == content
