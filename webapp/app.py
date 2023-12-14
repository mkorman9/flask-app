from flask import request
from pydantic import BaseModel, constr
from uuid_extensions import uuid7str

from webapp.base import app


class TodoItemModel(BaseModel):
    content: constr(min_length=1)


items = [{'id': '0657a144-93c6-77b2-8000-c7926fdd3686', 'content': 'Test Item'}] if app.config['TEST_DATA'] else []


@app.get('/api/items')
def get_todo_items():
    return items


@app.post('/api/items')
def create_todo_item():
    payload = TodoItemModel(**request.get_json())

    item_id = uuid7str()
    items.append({'id': item_id, 'content': payload.content})

    return {'id': item_id}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
