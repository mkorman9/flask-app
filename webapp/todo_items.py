from typing import Optional, List

from psycopg.errors import InvalidTextRepresentation
from uuid_extensions import uuid7str

from webapp.db import pool


class TodoItem(object):
    def __init__(self, item_id: str, content: str):
        self.item_id = item_id
        self.content = content


class TodoItemsPage(object):
    def __init__(self, data: List[TodoItem], page_size: int, next_page_token: Optional[str] = None):
        self.data = data
        self.page_size = page_size
        self.next_page_token = next_page_token


def find_todo_items_page(page_size: int, page_token: Optional[str] = None) -> TodoItemsPage:
    try:
        with pool.connection() as conn:
            if page_token:
                query = ('select id, content from todo_items where id > %s limit %s', (page_token, page_size,))
            else:
                query = ('select id, content from todo_items limit %s', (page_size,))

            with conn.execute(*query) as result:
                data = [TodoItem(item_id=str(record[0]), content=record[1]) for record in result.fetchall()]
                next_page_token = str(data[len(data) - 1].item_id) if len(data) > 0 else None
                return TodoItemsPage(data=data, page_size=page_size, next_page_token=next_page_token)
    except InvalidTextRepresentation:
        return TodoItemsPage(data=[], page_size=page_size, next_page_token=None)


def find_todo_item(item_id: str) -> Optional[TodoItem]:
    try:
        with pool.connection() as conn:
            with conn.execute('select id, content from todo_items where id = %s', (item_id,)) as result:
                item = result.fetchone()
                if not item:
                    return None
                return TodoItem(item_id=str(item[0]), content=item[1])
    except InvalidTextRepresentation:
        return None


def add_todo_item(content: str) -> str:
    item_id = uuid7str()
    with pool.connection() as conn:
        conn.execute('insert into todo_items (id, content) values (%s, %s)', (item_id, content))
        return item_id


def delete_todo_item(item_id: str) -> bool:
    try:
        with pool.connection() as conn:
            with conn.execute('delete from todo_items where id = %s', (item_id,)) as result:
                return result.rowcount > 0
    except InvalidTextRepresentation:
        return False


def update_todo_item(item_id: str, content: str) -> bool:
    try:
        with pool.connection() as conn:
            with conn.execute('update todo_items set content = %s where id = %s', (content, item_id)) as result:
                return result.rowcount > 0
    except InvalidTextRepresentation:
        return False


def delete_all_todo_items():
    with pool.connection() as conn:
        conn.execute('delete from todo_items')
