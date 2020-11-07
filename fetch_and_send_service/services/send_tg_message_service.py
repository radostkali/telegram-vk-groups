from telegram.ext import CallbackContext

import telegram_service.constants
from fetch_and_send_service.services.vk_post_to_tg_message_service import TgMessageDTO


class SendTgMessageService:

    def __init__(self, callback_context: CallbackContext) -> None:
        self.callback_context = callback_context

    def _send_photo(self, message_dto: TgMessageDTO) -> None:
        self.callback_context.bot.send_photo(**message_dto.payload)

    def _send_text(self, message_dto: TgMessageDTO) -> None:
        self.callback_context.bot.send_message(**message_dto.payload)

    def _send_group(self, message_dto: TgMessageDTO) -> None:
        self.callback_context.bot.send_media_group(**message_dto.payload)

    def execute(self, message_dto: TgMessageDTO) -> None:
        if message_dto.media_type == telegram_service.constants.MEDIA_TYPE_TEXT:
            self._send_text(message_dto)
        elif message_dto.media_type == telegram_service.constants.MEDIA_TYPE_PHOTO:
            self._send_photo(message_dto)
        elif message_dto.media_type == telegram_service.constants.MEDIA_TYPE_GROUP:
            self._send_group(message_dto)
