from telegram.update import Update
from telegram.ext import CallbackContext

from database.daos.user_dao import UserDTO
from telegram_service.services.check_or_create_user_service import CheckOrCreateUserService

import telegram_service.constants
from telegram_service.command_handlers.base_command_handler import BaseCommandHandler


class StartCommandHandler(BaseCommandHandler):
    STAGE = telegram_service.constants.STAGE_LISTENING
    COMMAND = 'start'

    @classmethod
    def _get_commands_html_list(cls) -> str:
        command_html_raw_list = []
        for command, description in telegram_service.constants.COMMANDS_DESCRIPTIONS_LIST.items():
            command_html_raw_list.append(
                f'<b>{command}</b> - {description}'
            )

        commands_html_list = '\n'.join(command_html_raw_list)
        return commands_html_list

    @classmethod
    def callback(cls, update: Update, context: CallbackContext) -> None:
        context.user_data.update({'stage': cls.STAGE})

        update.message.reply_text(text='Кулити 🤙')

        user_dto = UserDTO(
            user_id=update.effective_chat.id,
            login=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )
        check_or_create_user_service = CheckOrCreateUserService()
        check_or_create_user_service.execute(user_dto=user_dto)

        update.message.reply_text(
            text='Добавляй в список любимые паблики и наслаждайся мемами, дурачье 🤝'
        )
        update.message.reply_text(
            text=f'🧠 Доступные команды:\n'
                 f'{cls._get_commands_html_list()}',
            parse_mode='HTML',
        )
