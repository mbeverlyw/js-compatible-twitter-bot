import logging
from logging.handlers import RotatingFileHandler

from .config import ScraperConfig as Config


CONFIG = Config()


def get_logger(name):
    print(f"Getting logger for {name}")
    logger = Logger(name)
    return logger.get_logger_instance()


class Logger:
    def __init__(self, name):
        self.logger = self.setup_logger(name)

    def setup_logger(self, name):
        # Set up logfile and message logging.
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Create the rotating file handler. Limit the size to 1000000Bytes ~ 1MB .
        handler = RotatingFileHandler(
            CONFIG.get_logger_path(), 
            mode='a+', 
            maxBytes=CONFIG.get_logger_size(), 
            backupCount=CONFIG.get_logger_max_rollover(), 
            encoding='utf-8', delay=0)
        handler.setLevel(logging.DEBUG)

        # Create a formatter.
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s {%(funcName)s:%(lineno)d}] [%(levelname)s]: %(message)s')

        # Add handler and formatter.
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        print(f"Logger has been setup")

        return logger
    
    def get_logger_instance(self):
        return self.logger
