from flask_sock import Sock


def register(sock: Sock):
    @sock.route('/ws')
    def websocket_endpoint(ws):
        print('websocket connected')

        while True:
            data = ws.receive(timeout=10)
            if not data:
                ws.close()
                break

            print('websocket message:', data)
            if data == 'close':
                ws.close()
                break

            ws.send(data)

        print('websocket disconnected')
