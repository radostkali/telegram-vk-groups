from typing import List

from db.db_crud_dao import DBCrudDAO, UserPublicRefreshDTO
from vk import VkAPI

from telegram.ext import CallbackContext
from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup


class SendFreshPostsService:

    MEDIA_TYPE_PHOTO = 'photo'
    MEDIA_TYPE_TEXT = 'text'
    MEDIA_TYPE_GROUP = 'group'

    POST_COMMENTS_BUTTON_TEXT = 'See comments'

    def __init__(self, callback_context: CallbackContext) -> None:
        self.callback_context = callback_context

    def _get_comment_markup(self, public_id: int, post_id: int) -> InlineKeyboardMarkup:
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

    def _get_post_message(
            self,
            post: Dict[str, Union[int, str, List[str], bool]],
            user_id: int,
            pub_name: str,
            pub_id: int) -> Optional[Tuple[str, Dict[str, Any]]]:
        message_payload = {
            'chat_id': user_id,
            'parse_mode': 'HTML',
            'reply_markup': self._get_comment_markup(
                public_id=pub_id,
                post_id=post['id'],
            )
        }
        if post['is_pinned']:
            return None
        elif len(post['pictures']) == 0:
            media_type = self.MEDIA_TYPE_TEXT
            message_payload['disable_web_page_preview'] = True
            message_payload['text'] = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
        elif len(post['pictures']) == 1:
            media_type = self.MEDIA_TYPE_PHOTO
            message_payload['caption'] = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
            message_payload['photo'] = post['pictures'][0]
        elif len(post['pictures']) > 1:
            media_type = self.MEDIA_TYPE_GROUP
            message_payload['media'] = [InputMediaPhoto(media=url) for url in post['pictures']]
            message_payload['media'][0].caption = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
            message_payload['media'][0].parse_mode = 'HTML'
        else:
            return None
        return media_type, message_payload

    def _prepare_posts(self, user_publics_refresh_dto_list: List[UserPublicRefreshDTO]) -> List:
        for user_publics_refresh_dto in user_publics_refresh_dto_list:
            publics_dto_list = user_publics_refresh_dto.publics
            for public_dto in publics_dto_list:
                users_publics[user_id]['publics'][pub_id]['posts'] = VkAPI.fetch_fresh_posts(pub_id, last_refresh)
                for post in users_publics[user_id]['publics'][pub_id]['posts']:
                    post_to_send = get_post_message(
                        post=post,
                        user_id=user_id,
                        pub_name=users_publics[user_id]['publics'][pub_id]['name'],
                        pub_id=pub_id,
                    )
                    posts_to_send.append(post_to_send)
            update_user_last_refresh(user_id)
        return posts_to_send

    def execute(self):
        user_publics_refresh_dto_list = DBCrudDAO.get_users_publics_to_refresh()
        posts = self._prepare_posts(
            user_publics_refresh_dto_list=user_publics_refresh_dto_list
        )
        for post in posts:
            if post:
                MESSAGE_MEDIA_TYPES[post[0]](context, post[1])
                time.sleep(1)