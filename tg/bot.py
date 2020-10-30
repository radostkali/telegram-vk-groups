import logging
from typing import Tuple, Callable

from tg.commands import HANDLERS
from tg.scheduler import SCHEDULERS

import settings

from telegram.ext import Updater, Dispatcher, JobQueue, Handler


class TgBot:

    def __init__(self) -> None:
        self.updater = Updater(
            token=settings.TG_BOT_TOKEN,
            use_context=True,
        )
        self._add_handlers(
            dispatcher=self.updater.dispatcher,
            handlers=HANDLERS,
        )
        self._run_scheduler(
            job_queue=self.updater.job_queue,
            schedulers=SCHEDULERS,
        )

    def _add_handlers(
            self,
            dispatcher: Dispatcher,
            handlers: Tuple[Handler]
    ) -> None:
        for command in handlers:
            dispatcher.add_handler(command)

    def _run_scheduler(
            self,
            job_queue: JobQueue,
            schedulers: Tuple[Tuple[Callable, int]]
    ) -> None:
        for callback, interval in schedulers:
            job_queue.run_repeating(callback, interval, first=0)

    def start(self):
        self.updater.start_polling()

        # self.updater.start_webhook(
        #     listen="0.0.0.0",
        #     port=int(HEROKU_PORT),
        #     url_path=TOKEN
        # )
        # self.updater.bot.setWebhook('https://{app}.herokuapp.com/{token}'.format(
        #     app=HEROKU_APP_NAME,
        #     token=TOKEN,
        # ))
        # self.updater.idle()

