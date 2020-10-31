from telegram import Update
from telegram.ext import CallbackContext

import telegram_service.constants
from telegram_service.text_handlers.add_text_handler import AddTextHandler
from telegram_service.text_handlers.delete_text_handler import DeleteTextHandler


class MessageStageHandler:
    @classmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        if context.user_data.get('stage') == telegram_service.constants.STAGE_ADDING:
            handler = AddTextHandler
        elif context.user_data.get('stage') == telegram_service.constants.STAGE_DELETING:
            handler = DeleteTextHandler
        else:
            return

        handler.execute(update, context)

        context.user_data.update({'stage': handler.SET_STAGE})
