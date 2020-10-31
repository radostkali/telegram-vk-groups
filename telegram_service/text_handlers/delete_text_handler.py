from telegram.update import Update
from telegram.ext import CallbackContext

from database.daos.user_public_dao import UserPublicDAO

import telegram_service.constants
from telegram_service.command_handlers.add_command_handler import AddCommandHandler
from telegram_service.command_handlers.delete_command_handler import DeleteCommandHandler
from telegram_service.text_handlers.base_text_stage_handler import BaseTextStageHandler
from telegram_service.services.get_user_publics_html_list_service import GetUserPublicsHtmlList


class DeleteTextHandler(BaseTextStageHandler):
    TRIGGER_STAGE = telegram_service.constants.STAGE_DELETING
    SET_STAGE = telegram_service.constants.STAGE_LISTENING

    @classmethod
    def execute(cls, update: Update, context: CallbackContext) -> None:
        publics_numbers = str(update.message.text).replace(
            '\n', ' '
        ).replace(
            ',', ' '
        ).split(' ')
        public_dto_list = UserPublicDAO.get_user_publics(user_id=update.effective_chat.id)

        for raw_public_number in publics_numbers:
            try:
                public_number = int(raw_public_number)
            except ValueError:
                continue

            if not 0 < public_number <= len(public_dto_list):
                continue

            UserPublicDAO.remove_user_public(
                user_id=update.effective_chat.id,
                public_id=public_dto_list[public_number - 1].public_id,
            )

        get_user_publics_html_list_service = GetUserPublicsHtmlList()
        publics_html_list = get_user_publics_html_list_service.execute(
            user_id=update.effective_chat.id
        )

        if not publics_html_list:
            update.message.reply_text(
                text=f'Список подписок пуст.\n'
                     f'Чтобы подписаться на паблик жми /{AddCommandHandler.COMMAND}'
            )
            return

        update.message.reply_text(
            text=f'Твои подписки::\n'
                 f'{publics_html_list}\n\n'
                 f'Добавить паблик: /{AddCommandHandler.COMMAND}\n'
                 f'Отписаться: /{DeleteCommandHandler.COMMAND}',
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
