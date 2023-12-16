from flask import Blueprint, request
from pydantic import BaseModel, constr

from webapp.todo_items import find_todo_items_page, add_todo_item, delete_todo_item, update_todo_item, find_todo_item

api = Blueprint('todo_items_api', __name__)


class TodoItemModel(BaseModel):
    content: constr(min_length=1)


@api.get('/api/items')
def get_items():
    page_size = request.args.get('page_size', default=10, type=int)
    page_token = request.args.get('page_token', default=None, type=str)

    page = find_todo_items_page(page_size, page_token)

    return {
        'data': [{
            'id': str(item.item_id),
            'content': item.content
        } for item in page.data],
        'page_size': page.page_size,
        'next_page_token': page.next_page_token
    }


@api.get('/api/items/<item_id>')
def get_item(item_id):
    item = find_todo_item(item_id)
    if not item:
        return {
            'title': 'Item with given id does not exist',
            'type': 'ItemNotFound'
        }, 404

    return {
        'id': str(item.item_id),
        'content': item.content
    }


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


@api.put('/api/items/<item_id>')
def update_item(item_id):
    payload = TodoItemModel(**request.get_json())

    updated = update_todo_item(item_id, payload.content)
    if not updated:
        return {
            'title': 'Item with given id does not exist',
            'type': 'ItemNotFound'
        }, 404

    return {
        'status': 'success'
    }
