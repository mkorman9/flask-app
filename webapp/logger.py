import logging
import os

import gevent


def configure_logger():
    logging.basicConfig(
        level=os.getenv('LOG_LEVEL', 'INFO'),
        format='[%(levelname)s] %(message)s'
    )

    # Mute gevent exceptions
    gevent.get_hub().exception_stream = None
