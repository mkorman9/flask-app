import logging

from webapp.config import config

logging.basicConfig(level=logging.NOTSET)
logging.root.handlers.clear()

__formatter = logging.Formatter('[%(levelname)s] %(message)s')

__handler = logging.StreamHandler()
__handler.setLevel(config.LOG_LEVEL)
__handler.setFormatter(__formatter)

log = logging.getLogger('app')
log.addHandler(__handler)
