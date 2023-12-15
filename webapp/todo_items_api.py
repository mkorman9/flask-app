from flask import Blueprint, request
from pydantic import BaseModel, constr

from webapp.todo_items import find_todo_items, add_todo_item, delete_todo_item

api = Blueprint('todo_items_api', __name__)


class TodoItemModel(BaseModel):
    content: constr(min_length=1)


@api.get('/api/items')
def get_items():
    return [item.__dict__ for item in find_todo_items()]


@api.post('/api/items')
def create_item():
    payload = TodoItemModel(**request.get_json())

    item_id = add_todo_item(payload.content)
    return {'id': item_id}


@api.delete('/api/items/<item_id>')
def delete_item(item_id):
    deleted = delete_todo_item(item_id)
    if not deleted:
        return {
            'title': 'Item with given id does not exist',
            'type': 'ItemNotFound'
        }, 404

    return {
        'status': 'success'
    }
