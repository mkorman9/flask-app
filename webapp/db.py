import atexit
from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from webapp.config import get_config

_engine: Optional[Engine] = None


def session():
    global _engine

    if not _engine:
        raise RuntimeError('DB engine is closed')

    return Session(_engine)


def open_pool():
    global _engine

    c = get_config()
    _engine = create_engine(
        c.DB_URL,
        pool_size=c.DB_POOL_SIZE,
        pool_timeout=10
    )

    atexit.register(_close_pool)


def _close_pool():
    global _engine

    if not _engine:
        raise RuntimeError('DB engine is closed')

    _engine.dispose()
    _engine = None
