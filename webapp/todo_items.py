import uuid
from typing import Optional, List, Tuple, Any

from psycopg.errors import InvalidTextRepresentation
from uuid_extensions import uuid7

from webapp.db import pool


class TodoItem(object):
    def __init__(self, item_id: uuid.UUID, content: str):
        self.item_id = item_id
        self.content = content


class TodoItemsPage(object):
    def __init__(
        self,
        data: List[TodoItem],
        page_size: int,
        next_page_token: Optional[uuid.UUID] = None
    ):
        self.data = data
        self.page_size = page_size
        self.next_page_token = next_page_token


def find_todo_items_page(
    page_size: int,
    page_token: Optional[str] = None
) -> TodoItemsPage:
    with pool.connection() as conn:
        if page_token:
            query: Tuple[str, Tuple[Any, ...]] = (
                'select id, content from todo_items where id > %s limit %s',
                (page_token, page_size)
            )
        else:
            query = (
                'select id, content from todo_items limit %s',
                (page_size,)
            )

        try:
            with conn.execute(*query) as result:
                data = [
                    TodoItem(
                        item_id=record[0],
                        content=record[1]
                    )
                    for record in result.fetchall()
                ]

                if len(data) > 0:
                    next_page_token = data[len(data) - 1].item_id
                else:
                    next_page_token = None

                return TodoItemsPage(
                    data=data,
                    page_size=page_size,
                    next_page_token=next_page_token
                )
        except InvalidTextRepresentation:
            return TodoItemsPage(
                data=[],
                page_size=page_size,
                next_page_token=None
            )


def find_todo_item(item_id: str) -> Optional[TodoItem]:
    with pool.connection() as conn:
        try:
            with conn.execute(
                'select id, content from todo_items where id = %s',
                (item_id,)
            ) as result:
                record = result.fetchone()
                if not record:
                    return None
                return TodoItem(item_id=record[0], content=record[1])
        except InvalidTextRepresentation:
            return None


def add_todo_item(content: str) -> uuid.UUID:
    item_id = uuid7()
    with pool.connection() as conn:
        conn.execute(
            'insert into todo_items (id, content) values (%s, %s)',
            (str(item_id), content)
        )
        return item_id


def delete_todo_item(item_id: str) -> bool:
    with pool.connection() as conn:
        try:
            with conn.execute(
                'delete from todo_items where id = %s',
                (item_id,)
            ) as result:
                return result.rowcount > 0
        except InvalidTextRepresentation:
            return False


def update_todo_item(item_id: str, content: str) -> bool:
    with pool.connection() as conn:
        try:
            with conn.execute(
                'update todo_items set content = %s where id = %s',
                (content, item_id)
            ) as result:
                return result.rowcount > 0
        except InvalidTextRepresentation:
            return False


def delete_all_todo_items():
    with pool.connection() as conn:
        conn.execute('delete from todo_items')
