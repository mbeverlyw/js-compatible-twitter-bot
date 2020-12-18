from ..config import ScraperConfig as Config
from ._base import Database
from .login_activity import LoginActivity
from .notifications import Notifications


def initialize_db():
    print("Instance of creating db tables...")
    Database().create_db_tables()
