import os
import sys
from typing import Optional

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel


class ConfigModel(BaseModel):
    TEST_DATA: Optional[bool] = False


try:
    load_dotenv()
    values = ConfigModel(**os.environ)
except ValidationError as e:
    print('Failed to load configuration:', e)
    sys.exit(1)
