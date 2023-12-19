from flask_sock import Sock

from webapp.base import create_app_base
from webapp.healthcheck import healthcheck_api
from webapp.todo_items import todo_items_api
from webapp.websocket import websocket_api

app = create_app_base(__name__)
websockets = Sock(app)

app.register_blueprint(healthcheck_api.blueprint)
app.register_blueprint(todo_items_api.blueprint)
websocket_api.register(websockets)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
