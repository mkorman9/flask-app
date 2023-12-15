from typing import Generator

from psycopg.errors import InvalidTextRepresentation
from uuid_extensions import uuid7str

from webapp.db import pool


class TodoItem:
    def __init__(self, item_id, content):
        self.id = item_id
        self.content = content


def find_todo_items() -> Generator[TodoItem, None, None]:
    with pool.connection() as conn:
        with conn.execute('select id, content from todo_items') as result:
            return (TodoItem(item_id=record[0], content=record[1]) for record in result.fetchall())


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


def delete_all_todo_items():
    with pool.connection() as conn:
        conn.execute('delete from todo_items')
