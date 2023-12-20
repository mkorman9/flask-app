import os

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


__postgres = DockerContainer('postgres:15')


def pytest_configure(config):
    global __postgres

    db_name = 'test_db'
    db_user = 'test_user'
    db_password = 'test_password'

    __postgres.with_exposed_ports(5432)
    __postgres.with_env('POSTGRES_DB', db_name)
    __postgres.with_env('POSTGRES_USER', db_user)
    __postgres.with_env('POSTGRES_PASSWORD', db_password)
    __postgres.with_volume_mapping(
        f'{os.getcwd()}/migrations',
        '/docker-entrypoint-initdb.d',
        'ro'
    )

    __postgres.start()
    wait_for_logs(
        __postgres,
        'database system is ready to accept connections'
    )

    host = __postgres.get_container_host_ip()
    port = __postgres.get_exposed_port(5432)
    conn_str = f'{db_user}:{db_password}@{host}:{port}/{db_name}'
    os.environ['DB_URL'] = f'postgresql+psycopg://{conn_str}'


def pytest_unconfigure(config):
    global __postgres

    __postgres.stop()
