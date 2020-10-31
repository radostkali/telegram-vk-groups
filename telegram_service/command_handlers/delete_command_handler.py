from telegram.update import Update
from telegram.ext import CallbackContext

import telegram_service.constants
from telegram_service.command_handlers.base_command_handler import BaseCommandHandler
from telegram_service.command_handlers.add_command_handler import AddCommandHandler
from telegram_service.services.get_user_publics_html_list_service import GetUserPublicsHtmlList


class DeleteCommandHandler(BaseCommandHandler):
    STAGE = telegram_service.constants.STAGE_DELETING
    COMMAND = 'delete'

    @classmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        get_user_publics_html_list_service = GetUserPublicsHtmlList()
        publics_html_list = get_user_publics_html_list_service.execute(
            user_id=update.effective_chat.id
        )
        if not publics_html_list:
            update.message.reply_text(
                text=f'Ты еще не подписался ни на один паблик.\n'
                     f'Чтобы добавить один жми /{AddCommandHandler.COMMAND}'
            )
            return

        context.user_data.update({'stage': cls.STAGE})
        update.message.reply_text(
            text=f'Напиши номера пабликов из списка, чтобы отписаться от них:\n'
                 f'{publics_html_list}',
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
