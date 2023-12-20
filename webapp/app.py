from flask_sock import Sock

from webapp import db
from webapp.flask_base_app import create_flask_base_app
from webapp.config import load_config
from webapp.healthcheck import healthcheck_api
from webapp.logger import configure_logger
from webapp.todo_items import todo_items_api
from webapp.websocket import websocket_api

configure_logger()
load_config()
db.open_connection_pool()

app = create_flask_base_app(__name__)
websockets = Sock(app)

app.register_blueprint(healthcheck_api.blueprint)
app.register_blueprint(todo_items_api.blueprint)
websocket_api.register(websockets)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
