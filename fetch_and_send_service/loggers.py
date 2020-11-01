import os
import logging
from logging.handlers import RotatingFileHandler
from abc import ABC, abstractmethod

import settings


class FetchAndSendBaseLogger(ABC):
    def __init__(self) -> None:
        self.logger = self._get_logger()

    @abstractmethod
    def _get_logger(self) -> logging.Logger:
        raise NotImplemented

    @abstractmethod
    def log(self, message) -> None:
        raise NotImplemented


class FetchAndSendDebugLogger(FetchAndSendBaseLogger):
    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('fetch_and_send_debug')
        handler = logging.StreamHandler()
        s_format = logging.Formatter('[%(name)s %(levelname)s] %(asctime)s: %(message)s')
        handler.setFormatter(s_format)
        logger.addHandler(handler)
        return logger

    def log(self, message) -> None:
        self.logger.info(message)


class FetchAndSendErrorLogger(FetchAndSendBaseLogger):
    LOG_FILEPATH = os.path.join(settings.BASEDIR, 'logs', 'fetch_and_send_error.log')

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('fetch_and_send')
        handler = RotatingFileHandler(
            self.LOG_FILEPATH,
            maxBytes=1024 * 1024 * 20,  # 20 mb
            backupCount=3,
        )
        s_format = logging.Formatter('[%(name)s %(levelname)s] %(asctime)s: %(message)s')
        handler.setFormatter(s_format)
        logger.addHandler(handler)
        return logger

    def log(self, message) -> None:
        self.logger.error(message)
