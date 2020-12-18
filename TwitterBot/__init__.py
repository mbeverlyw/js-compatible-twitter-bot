from .config import ActionsConfig, ScraperConfig
from .scraper import (
    followers,
    following,
    notifications,
)
from .db import initialize_db, Database


initialize_db()

