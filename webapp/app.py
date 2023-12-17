import atexit
import os

from flask_sock import Sock

from webapp import todo_items_api
from webapp import websocket_api
from webapp.base import create_app_base
from webapp.db import pool

try:
    from gevent import get_hub
    get_hub().exception_stream = None
except ImportError:
    pass

app = create_app_base(__name__)
websockets = Sock(app)


def on_startup():
    pool.open()

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
websocket_api.register(websockets)

on_startup()
atexit.register(on_shutdown)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
