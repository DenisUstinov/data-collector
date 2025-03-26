import os
from dotenv import load_dotenv

from .logger import setup_logger
from .models import Trade, Ticker, Order
from .config import DATABASE_URL, DATA
from .db import Database
from .client import Client
from .handler import Handler

ENV = os.getenv("ENV", "prod")
if ENV == "dev":
    load_dotenv()