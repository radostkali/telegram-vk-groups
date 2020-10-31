from dataclasses import dataclass
from typing import Callable, Tuple

from telegram.ext import CallbackContext

import settings

from fetch_and_send_service.factory import fetch_and_send_fresh_posts_usecase_factory


def send_fresh_posts_callback(context: CallbackContext) -> None:
    fetch_and_send_fresh_posts_usecase = fetch_and_send_fresh_posts_usecase_factory(
        callback_context=context
    )
    fetch_and_send_fresh_posts_usecase.execute()


@dataclass
class SchedulerDTO:
    callback: Callable
    interval: int  # in seconds


def get_telegram_schedulers() -> Tuple[SchedulerDTO]:
    schedulers = (
        SchedulerDTO(
            callback=send_fresh_posts_callback,
            interval=settings.TG_SEND_FRESH_POSTS_IN_EVERY_SECONDS,
        ),
    )
    return schedulers
