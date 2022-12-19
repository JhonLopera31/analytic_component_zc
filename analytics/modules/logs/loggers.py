from logging.config import dictConfig
from logging import getLogger
from config.settings import LOGGING_SETTINGS


class GeneralLogger:
    _logger = None

    @classmethod
    def setup_logger(cls, log_stream_name):
        dictConfig(LOGGING_SETTINGS)
        cls._logger = getLogger(log_stream_name)

    @classmethod
    def put_log(cls, msg: str):
        cls._logger.info(msg)
