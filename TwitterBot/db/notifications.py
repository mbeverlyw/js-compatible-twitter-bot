from ._base import NOTIFICATIONS, Database
from .._logger import get_logger

logger = get_logger(__name__)


class Notifications(Database):
    def __init__(self):
        pass

    def insert_new_notification(self, tweet):
        """
        Appends a row to NOTIFICATIONS containing details on the
            unique tweet.
        """
        response_status = True if not tweet.is_queued else False

        # print(f"Inserting new Tweet")
        query = f"INSERT INTO {NOTIFICATIONS} " \
                f"(id, tweet_id, sender, text, request_type, " \
                f"response_status, timestamp) " \
                f"VALUES (NULL, '{tweet.id}', '{tweet.sender}', " \
                f"'{tweet.text}', '{tweet.command_found}', " \
                f"'{response_status}', datetime('now', 'localtime'));"

        self.execute_query(query)
        print(self.get_results(NOTIFICATIONS))
    
    def update_response_status(self, tweet_id):
        query = f"UPDATE {NOTIFICATIONS} " \
                f"set response_status=True " \
                f"WHERE tweet_id='{tweet_id}';"

        self.execute_query(query)

    def query_for_tweet_id(self, tweet_id):
        """
        Checks NOTIFICATIONS if the tweet_id has already been recorded. 
        """
        def _tweet_exists():
            num_of_results = len(results)

            return True if num_of_results > 0 else False
        
        def _get_response_status():
            return results[0]['response_status']

        tweet_found = False
        response_status = False

        query = f"SELECT * FROM {NOTIFICATIONS} " \
                f"WHERE tweet_id='{tweet_id}';"

        results = self.get_results(query=query)

        if _tweet_exists():
            # Check if the tweet has already been processed 
            # via response_status
            tweet_found = True
            response_status = _get_response_status()
        
        return tweet_found, response_status

