from typing import List

from telegram.ext import CommandHandler, Handler

from telegram_service.command_handlers.start_command_handler import StartCommandHandler
from telegram_service.command_handlers.add_command_handler import AddCommandHandler
from telegram_service.command_handlers.list_command_handler import ListCommandHandler
from telegram_service.command_handlers.delete_command_handler import DeleteCommandHandler
from telegram_service.command_handlers.help_command_handler import HelpCommandHandler


CUSTOM_COMMAND_HANDLERS = (
    AddCommandHandler,
    DeleteCommandHandler,
    HelpCommandHandler,
    ListCommandHandler,
    StartCommandHandler,
)


def get_command_handlers() -> List[Handler]:
    handlers = [
        CommandHandler(
            command=custom_command_handler.COMMAND,
            callback=custom_command_handler.callback,
        ) for custom_command_handler in CUSTOM_COMMAND_HANDLERS
    ]
    return handlers
