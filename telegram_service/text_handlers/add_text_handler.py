from telegram.update import Update
from telegram.ext import CallbackContext

from vk_service.services import VkGetPublicService

import telegram_service.constants
from telegram_service.command_handlers.add_command_handler import AddCommandHandler
from telegram_service.command_handlers.delete_command_handler import DeleteCommandHandler
from telegram_service.command_handlers.list_command_handler import ListCommandHandler
from telegram_service.text_handlers.base_text_stage_handler import BaseTextStageHandler
from telegram_service.services.try_find_publics_service import TryFindPublicsService
from telegram_service.services.subscribe_user_to_public_service import SubscribeUserToPublicService


class AddTextHandler(BaseTextStageHandler):
    TRIGGER_STAGE = telegram_service.constants.STAGE_ADDING
    SET_STAGE = telegram_service.constants.STAGE_LISTENING

    @classmethod
    def execute(cls, update: Update, context: CallbackContext) -> None:
        vk_get_public_service = VkGetPublicService()
        try_find_public_service = TryFindPublicsService(
            vk_get_public_service=vk_get_public_service
        )
        subscribe_user_to_public_service = SubscribeUserToPublicService()

        found_publics_dto = try_find_public_service.execute(
            raw_publics_list=update.message.text
        )

        success_founded_publics_html = ''
        if found_publics_dto.retrieved_public_dto_list:

            founded_publics_html_rows = []
            for public_number, public_dto in enumerate(found_publics_dto.retrieved_public_dto_list, start=1):
                subscribe_user_to_public_service.execute(
                    user_id=update.effective_chat.id,
                    public_dto=public_dto,
                )
                public_html_row = '{num}. <a href="https://vk.com/{slug}">{name}</a> (<code>{slug}</code>)'.format(
                    num=public_number,
                    slug=public_dto.public_slug_url,
                    name=public_dto.public_name,
                )
                founded_publics_html_rows.append(public_html_row)

            founded_publics_html_list = '\n'.join(founded_publics_html_rows)
            success_founded_publics_html = f'👌 Оформили подписку на:\n' \
                                           f'{founded_publics_html_list}'

        not_found_publics_html = ''
        if found_publics_dto.not_found_publics:
            not_found_publics_html_list = '\n'.join(
                [f'<code>{slug}</code>' for slug in found_publics_dto.not_found_publics]
            )
            not_found_publics_html = f'🤔 Паблики, которые не удалось найти по указаным ссылкам или id: \n' \
                                     f'{not_found_publics_html_list}'

        update.message.reply_text(
            text=f'{success_founded_publics_html}\n\n'
                 f'{not_found_publics_html}\n\n'
                 f'Список пабликов: /{ListCommandHandler.COMMAND}\n'
                 f'Добавить паблик: /{AddCommandHandler.COMMAND}\n'
                 f'Отписаться: /{DeleteCommandHandler.COMMAND}',
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
