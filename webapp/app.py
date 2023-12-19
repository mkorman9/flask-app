import atexit
import logging
import os

from flask_sock import Sock

from webapp import db
from webapp.base import create_app_base
from webapp.healthcheck import healthcheck_api
from webapp.todo_items import todo_items_api
from webapp.websocket import websocket_api

app = create_app_base(__name__)
websockets = Sock(app)

app.register_blueprint(healthcheck_api.blueprint)
app.register_blueprint(todo_items_api.blueprint)
websocket_api.register(websockets)


def on_startup():
    db.open_pool()

    logging.info('✅ Worker is ready (PID=%d)', os.getpid())


def on_shutdown():
    db.close_pool()

    logging.info('⛔ Worker is shutting down (PID=%d)', os.getpid())


on_startup()
atexit.register(on_shutdown)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
