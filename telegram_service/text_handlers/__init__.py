from typing import List

from telegram.ext import MessageHandler, Filters, Handler

from telegram_service.text_handlers.message_stage_handler import MessageStageHandler


def get_text_handlers() -> List[Handler]:
    handlers = [
        MessageHandler(
            filters=Filters.text,
            callback=MessageStageHandler.callback,
        )
    ]
    return handlers
