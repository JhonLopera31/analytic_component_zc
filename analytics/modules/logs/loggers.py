import logging.config
from logging import getLogger
from logging import Logger
from config.settings import LOGGING_SETTINGS


class GeneralLogger:

    _logger: Logger = None

    @classmethod
    def setup_logger(cls, log_stream_name):
        logging.config.dictConfig(LOGGING_SETTINGS)
        cls._logger = getLogger(log_stream_name)

    @classmethod
    def get_logger(cls):
        return cls._logger

    @classmethod
    def put_log(cls, msg: str):
        cls._logger.info(msg)
