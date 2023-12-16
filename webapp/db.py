import logging

from psycopg_pool import ConnectionPool

from webapp.config import config

logging.getLogger("psycopg.pool").setLevel('ERROR')


def __reconnect_failed(p):
    print('🚫 Reconnect to the database has failed')


pool = ConnectionPool(
    config.DB_URL,
    min_size=config.DB_POOL_MIN,
    max_size=config.DB_POOL_MAX,
    open=False,
    timeout=10,
    reconnect_failed=__reconnect_failed,
)
