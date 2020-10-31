from typing import List

from telegram.ext import Handler

from telegram_service.text_handlers import get_text_handlers
from telegram_service.command_handlers import get_command_handlers


def get_handlers() -> List[Handler]:
    text_handlers_list = get_text_handlers()
    command_handlers_list = get_command_handlers()
    handlers = command_handlers_list + text_handlers_list

    return handlers
