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
    wait_for_logs(__postgres, 'database system is ready to accept connections')

    db_host_port = f'{__postgres.get_container_host_ip()}:{__postgres.get_exposed_port(5432)}'
    os.environ['DB_URL'] = f'postgresql://{db_user}:{db_password}@{db_host_port}/{db_name}'


def pytest_unconfigure(config):
    global __postgres

    __postgres.stop()
