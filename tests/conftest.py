import os

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


_postgres = DockerContainer('postgres:15')


def pytest_configure(config):
    global _postgres

    db_name = 'test_db'
    db_user = 'test_user'
    db_password = 'test_password'

    _postgres.with_exposed_ports(5432)
    _postgres.with_env('POSTGRES_DB', db_name)
    _postgres.with_env('POSTGRES_USER', db_user)
    _postgres.with_env('POSTGRES_PASSWORD', db_password)
    _postgres.with_volume_mapping(
        f'{os.getcwd()}/migrations',
        '/docker-entrypoint-initdb.d',
        'ro'
    )

    _postgres.start()
    wait_for_logs(
        _postgres,
        'database system is ready to accept connections'
    )

    host = _postgres.get_container_host_ip()
    port = _postgres.get_exposed_port(5432)
    conn_str = f'{db_user}:{db_password}@{host}:{port}/{db_name}'
    os.environ['DB_URL'] = f'postgresql+psycopg://{conn_str}'


def pytest_unconfigure(config):
    global _postgres

    _postgres.stop()
