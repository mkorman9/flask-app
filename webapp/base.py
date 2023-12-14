import sys
import traceback

from flask import Flask
from psycopg_pool import PoolTimeout
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from webapp.db import pool


def create_base_app() -> Flask:
    app = Flask(__name__)

    def on_start():
        try:
            pool.open(wait=True, timeout=10)
        except PoolTimeout:
            print('Failed to connect to the database: Timeout')
            __abort()

    def on_stop():
        pool.close()

    __register_hooks(on_start, on_stop)

    @app.errorhandler(ValidationError)
    def validation_error(e: ValidationError):
        return {
            'title': 'Provided request body contains schema violations',
            'type': 'ValidationError',
            'cause': [{'field': '.'.join(e['loc']), 'message': e['msg']} for e in e.errors()]
        }, 400

    @app.errorhandler(Exception)
    def internal_server_error(e):
        print('Uncaught exception:', traceback.format_exc())
        return {
            'title': 'Server has encountered an error when processing the request',
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
        elif e.code == 415:
            return {
                'title': 'Provided request body format was not recognised',
                'type': 'UnsupportedMediaType'
            }, 415
        return {
            'type': ''.join(e.name.split(' '))
        }, e.code

    return app


def __register_hooks(on_start, on_stop):
    try:
        from uwsgidecorators import postfork
        import uwsgi
        postfork(on_start)
        uwsgi.atexit = on_stop
    except ImportError:
        import atexit
        on_start()
        atexit.register(on_stop)


def __abort():
    try:
        import uwsgi
        uwsgi.stop()
    except ImportError:
        pass

    sys.exit(1)
