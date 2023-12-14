import os
import sys

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel


class ConfigModel(BaseModel):
    DB_URL: str


try:
    load_dotenv()
    config = ConfigModel(**os.environ)
except ValidationError as e:
    print('Failed to load configuration:', e)
    sys.exit(4)
