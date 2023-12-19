import logging

import gevent


def configure_logger():
    # Logging configuration for development run
    # Production config is defined in .gunicorn/logging.conf file
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] %(message)s'
    )

    # Mute gevent exceptions
    gevent.get_hub().exception_stream = None
