import logging

from tg.commands import HANDLERS
from tg.scheduler import SCHEDULERS
from settings import TG_BOT_TOKEN as TOKEN

from telegram.ext import Updater


class TgBot:

    def __init__(self, loglevel=logging.CRITICAL, *args, **kwargs):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self._add_commands()
        self._run_scheduler()

    def _add_commands(self):
        for command in HANDLERS:
            self.dispatcher.add_handler(command)

    def _run_scheduler(self):
        for scheduler in SCHEDULERS:
            self.job_queue.run_repeating(scheduler[0], interval=scheduler[1], first=0)

    def start(self):
        self.updater.start_polling()

