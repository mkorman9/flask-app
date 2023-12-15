import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel


class ConfigModel(BaseModel):
    DB_URL: str
    DB_POOL_MIN: int
    DB_POOL_MAX: int


try:
    load_dotenv()
    config = ConfigModel(**os.environ)
except ValidationError as e:
    print('Failed to load configuration:', e)
    sys.exit(4)
