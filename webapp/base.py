import logging

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from webapp.config import load_config
from webapp.logger import configure_logger


def create_app_base(import_name: str) -> Flask:
    app = Flask(import_name)

    configure_logger()
    load_config()

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
        logging.error(
            '🚫 Unhandled exception while processing the request',
            exc_info=e
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
