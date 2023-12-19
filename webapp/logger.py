import logging

import gevent

from webapp.config import config


def configure():
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='[%(levelname)s] %(message)s'
    )

    # Mute gevent exceptions
    gevent.get_hub().exception_stream = None
