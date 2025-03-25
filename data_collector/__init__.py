import os
from dotenv import load_dotenv

from .logger import setup_logger

ENV = os.getenv("ENV", "prod")
if ENV == "dev":
    load_dotenv()