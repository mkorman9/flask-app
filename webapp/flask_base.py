import traceback

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException


def create_base_app() -> Flask:
    app = Flask(__name__)

    __disable_gevent_exception_stream()

    @app.errorhandler(ValidationError)
    def validation_error(e: ValidationError):
        return {
            'title': 'Provided request body contains schema violations',
            'type': 'ValidationError',
            'cause': [{
                'location': e['loc'],
                'code': e['type'],
                'message': e['msg']
            } for e in e.errors()]
        }, 400

    @app.errorhandler(Exception)
    def internal_server_error(e):
        print(
            '🚫 Unhandled exception while processing the request:',
            traceback.format_exc()
        )
        return {
            'title':
                'Server has encountered an error when processing the request',
            'type': 'InternalServerError'
        }, 500

    @app.errorhandler(HTTPException)
    def generic_http_error(e: HTTPException):
        if e.code == 400:
            return {
                'title': 'Provided request cannot be parsed',
                'type': 'MalformedRequest'
            }, 400
        elif e.code == 404:
            return {
                'title': 'The request resource was not found',
                'type': 'NotFound'
            }, 404
        elif e.code == 405:
            return {
                'title': 'Requested method is not allowed',
                'type': 'MethodNotAllowed'
            }, 405
        elif e.code == 415:
            return {
                'title': 'Provided request body format was not recognised',
                'type': 'UnsupportedMediaType'
            }, 415
        return {
            'type': ''.join(e.name.split(' '))
        }, e.code

    return app


def __disable_gevent_exception_stream():
    try:
        from gevent import get_hub
        get_hub().exception_stream = None
    except ImportError:
        pass
