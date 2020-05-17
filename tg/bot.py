import logging

from tg.commands import HANDLERS
from tg.scheduler import SCHEDULERS
from settings import (
    TG_BOT_TOKEN as TOKEN,
    HEROKU_PORT,
    HEROKU_APP_NAME,
    DEBUG,
)

from telegram.ext import Updater


class TgBot:

    def __init__(self, loglevel=logging.CRITICAL, *args, **kwargs):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)
        self.updater = Updater(token=TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self._add_handlers()
        self._run_scheduler()

    def _add_handlers(self):
        for command in HANDLERS:
            self.dispatcher.add_handler(command)

    def _run_scheduler(self):
        for scheduler in SCHEDULERS:
            self.job_queue.run_repeating(scheduler[0], interval=scheduler[1], first=0)

    def start(self):
        if DEBUG:
            self.updater.start_polling()
        else:
            self.updater.start_webhook(
                listen="0.0.0.0",
                port=int(HEROKU_PORT),
                url_path=TOKEN
            )
            self.updater.bot.setWebhook('https://{app}.herokuapp.com/{token}'.format(
                app=HEROKU_APP_NAME,
                token=TOKEN,
            ))
            self.updater.idle()

