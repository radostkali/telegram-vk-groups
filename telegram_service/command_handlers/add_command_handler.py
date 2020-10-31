from telegram.update import Update
from telegram.ext import CallbackContext

import telegram_service.constants
from telegram_service.command_handlers.base_command_handler import BaseCommandHandler


class AddCommandHandler(BaseCommandHandler):
    STAGE = telegram_service.constants.STAGE_ADDING
    COMMAND = 'add'

    @classmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        context.user_data.update({'stage': cls.STAGE})

        update.message.reply_text(
            text='Укажи полный url паблика или его id (последнюю часть урла).\n'
                 'Также можешь указать список пабликов. Один паблик - одна строка.'
        )
        update.message.reply_text(
            text='Пример:\n'
                 '<code>https://vk.com/pikabu</code>\n'
                 '<code>pikabu</code>',
            parse_mode='HTML',
        )
