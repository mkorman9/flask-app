import logging

import gevent


def configure_logger(level: str):
    logging.basicConfig(
        level=level,
        format='[%(levelname)s] %(message)s'
    )

    # Mute gevent exceptions
    gevent.get_hub().exception_stream = None
