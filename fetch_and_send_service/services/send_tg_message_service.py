from typing import Any, Dict

from telegram.ext import CallbackContext

from fetch_and_send_service.services.vk_post_to_tg_message_service import TgMessageDTO


class SendTgMessageService:

    def __init__(self, callback_context: CallbackContext) -> None:
        self.callback_context = callback_context

    def _send_photo(self, payload: Dict[str, Any]) -> None:
        self.callback_context.bot.send_photo(**payload)

    def _send_text(self, payload: Dict[str, Any]) -> None:
        self.callback_context.bot.send_message(**payload)

    def _send_group(self, payload: Dict[str, Any]) -> None:
        self.callback_context.bot.send_media_group(**payload)

    def execute(self, message_dto: TgMessageDTO) -> None:
        if message_dto == TgMessageDTO.MEDIA_TYPE_TEXT:
            self._send_text(message_dto.payload)
        elif message_dto == TgMessageDTO.MEDIA_TYPE_PHOTO:
            self._send_photo(message_dto.payload)
        elif message_dto == TgMessageDTO.MEDIA_TYPE_GROUP:
            self._send_group(message_dto.payload)
