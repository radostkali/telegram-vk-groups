from dataclasses import dataclass
from typing import Any, Dict, Optional

from vk_service.api import PostDTO

from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup


@dataclass
class TgMessageDTO:

    MEDIA_TYPE_PHOTO = 'photo'
    MEDIA_TYPE_TEXT = 'text'
    MEDIA_TYPE_GROUP = 'group'

    media_type: Optional[str]
    payload: Dict[str, Any]


class VkPostToTgMessageService:

    POST_COMMENTS_BUTTON_TEXT = 'See comments'
    POST_TEXT_TEMPLATE = (
        '{text}\n'
        '\n'
        '<a href="https://vk.com/{public_slug}"><code>{public_name}</code>'
    )

    def _get_comment_btn_markup(self, public_id: int, post_id: int) -> InlineKeyboardMarkup:
        url_to_comments = 'https://vk.com/wall-{public_id}_{post_id}'.format(
            public_id=public_id,
            post_id=post_id,
        )
        comments_btn = InlineKeyboardButton(
            text=self.POST_COMMENTS_BUTTON_TEXT,
            url=url_to_comments,
        )
        markup = InlineKeyboardMarkup([[comments_btn]])
        return markup

    def execute(
            self,
            post: PostDTO,
            user_id: int,
            public_id: int,
            public_name: str,
            public_slug: str,
    ) -> TgMessageDTO:
        message_payload = {
            'chat_id': user_id,
            'parse_mode': 'HTML',
            'reply_markup': self._get_comment_btn_markup(
                public_id=public_id,
                post_id=post.id,
            )
        }
        message_text = self.POST_TEXT_TEMPLATE.format(
            text=post.text,
            public_slug=public_slug,
            public_name=public_name,
        )
        media_type = None

        pictures_number = len(post.pictures)
        if pictures_number == 0:
            media_type = TgMessageDTO.MEDIA_TYPE_TEXT
            message_payload.update({
                'text': message_text,
                'disable_web_page_preview': True,
            })
        elif pictures_number == 1:
            media_type = TgMessageDTO.MEDIA_TYPE_PHOTO
            message_payload.update({
                'caption': message_text,
                'photo': post.pictures[0],
            })
        elif pictures_number > 1:
            media_type = TgMessageDTO.MEDIA_TYPE_GROUP
            message_payload['media'] = [InputMediaPhoto(media=url) for url in post.pictures]
            message_payload['media'][0].caption = message_text
            message_payload['media'][0].parse_mode = 'HTML'

        message_dto = TgMessageDTO(
            media_type=media_type,
            payload=message_payload,
        )
        return message_dto
