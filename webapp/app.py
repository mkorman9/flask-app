from flask import request
from pydantic import BaseModel, constr

from webapp.base import create_base_app
from webapp.todo_items import find_todo_items, add_todo_item

app = create_base_app()


class TodoItemModel(BaseModel):
    content: constr(min_length=1)


@app.get('/api/items')
def get_todo_items():
    return list(find_todo_items())


@app.post('/api/items')
def create_todo_item():
    payload = TodoItemModel(**request.get_json())

    item_id = add_todo_item(payload.content)
    return {'id': item_id}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
