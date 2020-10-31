from telegram.update import Update
from telegram.ext import CallbackContext

import telegram_service.constants
from telegram_service.command_handlers.base_command_handler import BaseCommandHandler
from telegram_service.command_handlers.add_command_handler import AddCommandHandler
from telegram_service.command_handlers.delete_command_handler import DeleteCommandHandler
from telegram_service.services.get_user_publics_html_list_service import GetUserPublicsHtmlList


class ListCommandHandler(BaseCommandHandler):
    STAGE = telegram_service.constants.STAGE_LISTENING
    COMMAND = 'list'

    @classmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        context.user_data.update({'stage': cls.STAGE})

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

        update.message.reply_text(
            text=f'😎 Твои подписки:\n'
                 f'{publics_html_list}\n\n'
                 f'Добавить паблик: /{AddCommandHandler.COMMAND}\n'
                 f'Отписаться: /{DeleteCommandHandler.COMMAND}',
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
