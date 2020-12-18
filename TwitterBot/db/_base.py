from sqlalchemy import create_engine
from sqlalchemy import (
    Table, Column, Integer, String, Boolean, MetaData,
    ForeignKey, DateTime, BigInteger,
)
import datetime

from ..config import ScraperConfig as Config
from .._logger import get_logger

CONFIG = Config()
logger = get_logger(__name__)

# Table Names
LOGIN_ACTIVITY = 'loginActivity'  # logs the login activity
NOTIFICATIONS = 'notifications'  # table to handle notifications & statuses


class Database:
    DB_ENGINE = {
        CONFIG.get_database_type(): CONFIG.get_database_uri()
    }
    db_engine = None  # Main DB Connection Ref Obj

    def __init__(self, 
        dbtype=CONFIG.get_database_type(), 
        username='', password='', 
        dbname=CONFIG.get_database_uri()
        ):
        dbtype = dbtype.lower()

        logger.info("Initializing DB...")

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
        else:
            logger.error("DBType is not found in DB_ENGINE")
        
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

    def get_results(self, table=None, query=None):
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

