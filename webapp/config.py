import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel


class ConfigModel(BaseModel):
    DB_URL: str
    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 5


_config: Optional[ConfigModel] = None


def load_config():
    global _config

    try:
        load_dotenv()
        _config = ConfigModel(**os.environ)
    except ValidationError as e:
        logging.error('🚫 Failed to load configuration', exc_info=e)
        sys.exit(4)


def get_config():
    global _config

    if not _config:
        raise RuntimeError('Config is not loaded')

    return _config
