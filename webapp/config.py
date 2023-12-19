import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel


class ConfigModel(BaseModel):
    LOG_LEVEL: str = 'INFO'

    DB_URL: str
    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 5


try:
    load_dotenv()
    config = ConfigModel(**os.environ)
except ValidationError as e:
    print('🚫 Failed to load configuration:', e, file=sys.stderr)
    sys.exit(4)
