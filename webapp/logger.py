import logging
import os

import gevent


def configure_logger():
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
        force=True
    )

    # Mute gevent exceptions
    gevent.get_hub().exception_stream = None
