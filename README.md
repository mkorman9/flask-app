## Configure
```sh
make config
```

## Start locally
```sh
make run
```

## Run tests
```sh
make test
```

## Sidenotes

- This app is largely based on the template - https://github.com/mkorman9/flask-app-template
- Websocket support has been implemented by adding `flask-sock`
- Postgres support has been added with `psycopg[binary]` and `psycopg[pool]`.
`testcontainers` have been used for tests (see `tests/conftest.py`)
