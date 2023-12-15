import atexit
import os
import sys

from psycopg_pool import PoolTimeout

from webapp import todo_items_api
from webapp.db import pool
from webapp.flask_base import create_base_app

app = create_base_app()


def on_startup():
    # open postgres connection pool
    try:
        pool.open(wait=True, timeout=10)
    except PoolTimeout:
        print('🚫 Failed to connect to the database: Timeout')
        sys.exit(4)

    print(f'✅ Worker is ready (PID={os.getpid()})')


def on_shutdown():
    pool.close()

    print(f'⛔ Worker is shutting down (PID={os.getpid()})')


@app.route('/')
def hello_world():
    return {
        'message': 'hello world'
    }


app.register_blueprint(todo_items_api.api)

on_startup()
atexit.register(on_shutdown)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
