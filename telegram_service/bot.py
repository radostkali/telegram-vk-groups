from typing import Iterable

from telegram_service import get_handlers
from telegram_service.scheduler import get_telegram_schedulers, SchedulerDTO

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
            handlers=get_handlers(),
        )
        self._run_scheduler(
            job_queue=self.updater.job_queue,
            schedulers=get_telegram_schedulers(),
        )

    def _add_handlers(
            self,
            dispatcher: Dispatcher,
            handlers: Iterable[Handler]
    ) -> None:
        for command in handlers:
            dispatcher.add_handler(command)

    def _run_scheduler(
            self,
            job_queue: JobQueue,
            schedulers: Iterable[SchedulerDTO]
    ) -> None:
        for scheduler_dto in schedulers:
            job_queue.run_repeating(
                callback=scheduler_dto.callback,
                interval=scheduler_dto.interval,
                first=0,
            )

    def start(self):
        self.updater.start_polling()
