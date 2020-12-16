from sqlalchemy import create_engine
from sqlalchemy import (
    Table, Column, Integer, String, Boolean, MetaData,
    ForeignKey, DateTime, BigInteger,
)
import datetime

from ..config import ScraperConfig as Config
from .._logger import get_logger

# Global Variables
CONFIG = Config()

# Table Names
LOGIN_ACTIVITY = 'loginActivity'  # logs the login activity
NOTIFICATIONS = 'notifications'  # table to handle notifications & statuses

logger = get_logger(__name__)


class Database:
    DB_ENGINE = {
        CONFIG.get_database_type(): CONFIG.get_database_uri()
    }
    db_engine = None  # Main DB Connection Ref Obj

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        logger.info("Initializing DB...")

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            # print(self.db_engine)
        else:
            # print("DBType is not found in DB_ENGINE")
            pass
        
        self.create_db_tables()


    def create_db_tables(self):
        metadata = MetaData()

        login_activity = Table(LOGIN_ACTIVITY, metadata,
                               Column('id',
                                      BigInteger().with_variant(Integer, 'sqlite'),
                                      primary_key=True),
                               Column('username', String),
                               Column('login_succeeded', Boolean),
                               Column('timestamp', DateTime),
                               )
        notifications = Table(NOTIFICATIONS, metadata,
                              Column('id',
                                     BigInteger().with_variant(Integer, 'sqlite'),
                                     primary_key=True),
                              Column('tweet_id', String),
                              Column('sender', String),
                              Column('text', String),
                              Column('request_type', String),
                              Column('response_status', Boolean),
                              Column('timestamp', DateTime),
                              )
        try:
            metadata.create_all(self.db_engine)
        except Exception as e:
            logger.error(e)
        
    def execute_query(self, query):
        """
        Executes the provided query.
        """
        with self.db_engine.connect() as conn:
            try:
                result = conn.execute(query)

            except Exception as e:
                logger.error(e)

                result = None
            
        return result

    def get_data(self, table=None, query=None):
        """
        Retrieves data of table or result of specific query.
        """
        def determine_query():
            """
            Determines the query by checking if a query arg was passed.
            """
            return query if query is not None \
                else f"SELECT * FROM '{table}';"

        def __to_list(__results):
            """
            Converts DB results to a (persistent) list.
            """
            rows = []
            for row in __results:
                rows.append(row)
            
            __results.close()

            return rows


        # Determine query and execute
        results = __to_list(self.execute_query(determine_query()))

        return results



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
        print(self.get_data(LOGIN_ACTIVITY))
    
    def insert_notification(self, tweet):
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
        print(self.get_data(NOTIFICATIONS))
    
    def update_notification_response_status(self, tweet_id):
        query = f"UPDATE {NOTIFICATIONS} " \
                f"set response_status=True " \
                f"WHERE tweet_id='{tweet_id}';"

        self.execute_query(query)

    def query_notifications_for_tweet_id(self, tweet_id):
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

        results = self.get_data(query=query)

        if _tweet_exists():
            # Check if the tweet has already been processed 
            # via response_status
            tweet_found = True
            response_status = _get_response_status()
        
        return tweet_found, response_status

