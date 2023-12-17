import uuid

from flask_sock import Sock
from simple_websocket.ws import Base

WS_PATH = '/ws'
WS_READ_TIMEOUT = 15


class WebSocketContext(object):
    def __init__(self, ws: Base):
        self.id = uuid.uuid4()
        self.ws = ws
        self.to_close = False

    def close(self):
        self.to_close = True

    def send(self, message: str | bytes):
        self.ws.send(message)


def on_connect(ctx: WebSocketContext):
    print('websocket connected', ctx.id)


def on_message(ctx: WebSocketContext, message: str | bytes):
    print(f'websocket message ({ctx.id}):', message)

    if message == 'close':
        ctx.close()
        return

    ctx.send(message)


def on_disconnect(ctx: WebSocketContext):
    print('websocket disconnected', ctx.id)


def register(sock: Sock):
    @sock.route(WS_PATH)
    def websocket_endpoint(ws: Base):
        ctx = WebSocketContext(ws)

        on_connect(ctx)

        while not ctx.to_close:
            message = ws.receive(timeout=WS_READ_TIMEOUT)
            if not message:
                break

            on_message(ctx, message)

        ws.close()
        on_disconnect(ctx)
