from uuid_extensions import uuid7str

from webapp.db import pool


def find_todo_items():
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, content from todo_items')
            for record in cursor.fetchall():
                yield {
                    'id': record[0],
                    'content': record[1]
                }


def add_todo_item(content: str) -> str:
    item_id = uuid7str()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO todo_items (id, content) VALUES (%s, %s)', (item_id, content))
            return item_id
