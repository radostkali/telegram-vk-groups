from telegram.update import Update
from telegram.ext import CallbackContext

import telegram_service.constants
from telegram_service.command_handlers.base_command_handler import BaseCommandHandler


class HelpCommandHandler(BaseCommandHandler):
    STAGE = telegram_service.constants.STAGE_LISTENING
    COMMAND = 'help'

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

        update.message.reply_text(
            text=f'🧠 Доступные команды:\n'
                 f'{cls._get_commands_html_list()}',
            parse_mode='HTML',
        )
