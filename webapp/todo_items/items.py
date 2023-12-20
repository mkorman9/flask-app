import uuid
from typing import Optional, List

from psycopg.errors import InvalidTextRepresentation
from sqlalchemy import String
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Mapped, mapped_column, \
    declarative_base
from uuid_extensions import uuid7

from webapp import db


class TodoItem(declarative_base()):
    __tablename__ = 'todo_items'

    id: Mapped[uuid.UUID] = mapped_column('id', primary_key=True)
    content: Mapped[str] = mapped_column('content', String(255))


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
    with db.session() as session:
        query = session.query(TodoItem)
        if page_token:
            query = query.filter(TodoItem.id > page_token)

        query = query.limit(page_size)

        try:
            data = query.all()

            if len(data) > 0:
                next_page_token = data[len(data) - 1].id
            else:
                next_page_token = None

            return TodoItemsPage(
                data=data,
                page_size=page_size,
                next_page_token=next_page_token
            )
        except DataError as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return TodoItemsPage(
                    data=[],
                    page_size=page_size,
                    next_page_token=None
                )
            raise e


def find_todo_item(item_id: str) -> Optional[TodoItem]:
    with db.session() as session:
        try:
            query = session.query(TodoItem).filter(TodoItem.id == item_id)
            return query.one_or_none()
        except DataError as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return None
            raise e


def add_todo_item(content: str) -> uuid.UUID:
    item_id = uuid7()
    with db.session() as session:
        item = TodoItem(id=item_id, content=content)
        session.add(item)
        session.commit()
        return item_id


def delete_todo_item(item_id: str) -> bool:
    with db.session() as session:
        try:
            affected_rows = session.query(
                TodoItem
            ).filter(
                TodoItem.id == item_id
            ).delete()

            session.commit()
            return affected_rows > 0
        except DataError as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return False


def update_todo_item(item_id: str, content: str) -> bool:
    with db.session() as session:
        try:
            affected_rows = session.query(
                TodoItem
            ).filter(
                TodoItem.id == item_id
            ).update({
                'content': content
            })

            session.commit()
            return affected_rows > 0
        except DataError as e:
            if isinstance(e.orig, InvalidTextRepresentation):
                return False
            raise e


def delete_all_todo_items():
    with db.session() as session:
        session.query(TodoItem).delete()
        session.commit()
