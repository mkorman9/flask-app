import logging

from psycopg_pool import ConnectionPool

from webapp.config import config

logging.getLogger("psycopg.pool").setLevel('ERROR')

pool = ConnectionPool(
    config.DB_URL,
    min_size=config.DB_POOL_MIN,
    max_size=config.DB_POOL_MAX,
    open=False,
    reconnect_timeout=5
)
