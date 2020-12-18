from ._base import LOGIN_ACTIVITY, Database
from .._logger import get_logger

logger = get_logger(__name__)


class LoginActivity(Database):
    def __init__(self):
        pass

    def insert_login_activity(self, username, login_succeeded):
        """
        Appends a row to LOGIN_ACITIVITY containing 
            login attempt details. 
        """
        query = f"INSERT INTO {LOGIN_ACTIVITY}" \
                f"(id, username, login_succeeded, timestamp) " \
                f"VALUES (NULL, '{username}', " \
                f"{login_succeeded}, datetime('now', 'localtime'));"

        self.execute_query(query)
        print(self.get_results(LOGIN_ACTIVITY))

    