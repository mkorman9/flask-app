import atexit
import logging
import os

from flask_sock import Sock

from webapp import todo_items_api, websocket_api
from webapp.base import configure_logger, create_app_base
from webapp.db import pool

configure_logger()
app = create_app_base(__name__)
websockets = Sock(app)


@app.route('/')
def hello_world():
    return {
        'message': 'hello world'
    }


app.register_blueprint(todo_items_api.api)
websocket_api.register(websockets)


def on_startup():
    pool.open()

    logging.info('✅ Worker is ready (PID=%d)', os.getpid())


def on_shutdown():
    pool.close()

    logging.info('⛔ Worker is shutting down (PID=%d)', os.getpid())


on_startup()
atexit.register(on_shutdown)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
