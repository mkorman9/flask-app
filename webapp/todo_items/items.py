import uuid
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
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
            try:
                page_token_uuid = uuid.UUID(page_token)
            except ValueError:
                return TodoItemsPage(
                    data=[],
                    page_size=page_size,
                    next_page_token=None
                )

            query = query.filter(TodoItem.id > page_token_uuid)

        query = query.limit(page_size)
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


def find_todo_item(item_id: str) -> Optional[TodoItem]:
    try:
        item_id_uuid = uuid.UUID(item_id)
    except ValueError:
        return None

    with db.session() as session:
        query = session.query(TodoItem).filter(TodoItem.id == item_id_uuid)
        return query.one_or_none()


def add_todo_item(content: str) -> uuid.UUID:
    item_id = uuid7()
    with db.session() as session:
        item = TodoItem(id=item_id, content=content)
        session.add(item)
        session.commit()
        return item_id


def delete_todo_item(item_id: str) -> bool:
    try:
        item_id_uuid = uuid.UUID(item_id)
    except ValueError:
        return False

    with db.session() as session:
        affected_rows = session.query(
            TodoItem
        ).filter(
            TodoItem.id == item_id_uuid
        ).delete()

        session.commit()
        return affected_rows > 0


def update_todo_item(item_id: str, content: str) -> bool:
    try:
        item_id_uuid = uuid.UUID(item_id)
    except ValueError:
        return False

    with db.session() as session:
        affected_rows = session.query(
            TodoItem
        ).filter(
            TodoItem.id == item_id_uuid
        ).update({
            'content': content
        })

        session.commit()
        return affected_rows > 0


def delete_all_todo_items():
    with db.session() as session:
        session.query(TodoItem).delete()
        session.commit()
