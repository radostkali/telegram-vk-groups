import os
import logging
from logging.handlers import RotatingFileHandler
from abc import ABC, abstractmethod

import settings


class VkApiBaseLogger(ABC):
    def __init__(self) -> None:
        self.logger = self._get_logger()

    @abstractmethod
    def _get_logger(self) -> logging.Logger:
        raise NotImplemented

    @abstractmethod
    def log(self, message) -> None:
        raise NotImplemented


class VkApiRequestDebugLogger(VkApiBaseLogger):
    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('vk_api_debug')
        handler = logging.StreamHandler()
        s_format = logging.Formatter('[%(name)s %(levelname)s] %(asctime)s: %(message)s')
        handler.setFormatter(s_format)
        logger.addHandler(handler)
        return logger

    def log(self, message) -> None:
        self.logger.info(message)


class VkApiErrorDebugLogger(VkApiBaseLogger):
    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('vk_api_debug')
        handler = logging.StreamHandler()
        s_format = logging.Formatter('[%(name)s %(levelname)s] %(asctime)s: %(message)s')
        handler.setFormatter(s_format)
        logger.addHandler(handler)
        return logger

    def log(self, message) -> None:
        self.logger.debug(message)


class VkApiRequestLogger(VkApiBaseLogger):
    LOG_FILEPATH = os.path.join(settings.BASEDIR, 'logs', 'vk_api_request.log')

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('vk_api_request')
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
        self.logger.info(message)


class VkApiErrorLogger(VkApiBaseLogger):
    LOG_FILEPATH = os.path.join(settings.BASEDIR, 'logs', 'vk_api_error.log')

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger('vk_api_error')
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
        self.logger.critical(message)
