import logging

from tg.commands import HANDLERS
from settings import TG_BOT_TOKEN as TOKEN

from telegram.ext import Updater


class TgBot:

    def __init__(self, loglevel=logging.CRITICAL, *args, **kwargs):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self._add_commands()

    def _add_commands(self):
        for command in HANDLERS:
            self.dispatcher.add_handler(command)

    def start(self):
        self.updater.start_polling()

