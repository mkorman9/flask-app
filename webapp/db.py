from psycopg_pool import ConnectionPool

from webapp.config import config

pool = ConnectionPool(
    config.DB_URL,
    open=False
)
