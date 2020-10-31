from abc import ABC, abstractmethod

from telegram.update import Update
from telegram.ext import CallbackContext


class BaseCommandHandler(ABC):

    @property
    @abstractmethod
    def STAGE(self):
        raise NotImplemented

    @property
    @abstractmethod
    def COMMAND(self):
        raise NotImplemented

    @classmethod
    @abstractmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        context.user_data.update({'stage': cls.STAGE})
        raise NotImplemented
