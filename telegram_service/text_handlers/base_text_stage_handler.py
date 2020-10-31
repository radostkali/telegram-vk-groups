from abc import ABC, abstractmethod

from telegram.update import Update
from telegram.ext import CallbackContext


class BaseTextStageHandler(ABC):

    @property
    @abstractmethod
    def TRIGGER_STAGE(self):
        raise NotImplemented

    @property
    @abstractmethod
    def SET_STAGE(self):
        raise NotImplemented

    @classmethod
    @abstractmethod
    def execute(cls, update: Update, context: CallbackContext) -> None:
        raise NotImplemented
