import atexit
import logging
from typing import Optional

from gevent.threading import Lock
from psycopg_pool import ConnectionPool

from webapp.config import get_config

_pool: Optional[ConnectionPool] = None
_lock = Lock()


def connection():
    global _pool, _lock

    with _lock:
        if not _pool:
            logging.getLogger('psycopg.pool').setLevel('ERROR')

            c = get_config()
            _pool = ConnectionPool(
                c.DB_URL,
                min_size=c.DB_POOL_MIN,
                max_size=c.DB_POOL_MAX,
                timeout=10,
                reconnect_failed=_reconnect_failed,
                open=True
            )

            atexit.register(_close_pool)

    return _pool.connection()


def _close_pool():
    global _pool

    if not _pool:
        raise RuntimeError('Pool is closed')

    _pool.close()
    _pool = None


def _reconnect_failed(p):
    logging.error('🚫 Reconnect to the database has failed')
