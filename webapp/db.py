import logging

from psycopg_pool import ConnectionPool

from webapp.config import config


logging.getLogger("psycopg.pool").setLevel('ERROR')

pool = ConnectionPool(
    config.DB_URL,
    open=False,
    reconnect_timeout=5,
)
