from typing import Optional, Dict, Union, List, Tuple, Any

from telegram.ext import CallbackContext
from telegram import InputMediaPhoto

from tg.markups import get_comment_markup


def send_photo(context, payload):
    # type: (CallbackContext, Dict[str]) -> None
    context.bot.send_photo(**payload)


def send_text(context, payload):
    # type: (CallbackContext, Dict[str]) -> None
    context.bot.send_message(**payload)


def send_group(context, payload):
    # type: (CallbackContext, Dict[str]) -> None
    context.bot.send_media_group(**payload)


MEDIA_PHOTO = 'photo'
MEDIA_TEXT = 'text'
MEDIA_GROUP = 'group'

MESSAGE_MEDIA_TYPES = {
    MEDIA_PHOTO: send_photo,
    MEDIA_TEXT: send_text,
    MEDIA_GROUP: send_group,
}


def get_post_message(post, user_id, pub_name, pub_id):
    # type: (Dict[str, Union[int, str, List[str], bool]], int, str, int) -> Optional[Tuple[str, Dict[str, Any]]]
    message_payload = {
        'chat_id': user_id,
        'parse_mode': 'HTML',
        'reply_markup': get_comment_markup(pub_id=pub_id, post_id=post['id'])
    }
    if post['is_pinned']:
        return None
    elif len(post['pictures']) == 0:
        media_type = MEDIA_TEXT
        message_payload['disable_web_page_preview'] = True
        message_payload['text'] = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
    elif len(post['pictures']) == 1:
        media_type = MEDIA_PHOTO
        message_payload['caption'] = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
        message_payload['photo'] = post['pictures'][0]
    elif len(post['pictures']) > 1:
        media_type = MEDIA_GROUP
        message_payload['media'] = [InputMediaPhoto(media=url) for url in post['pictures']]
        message_payload['media'][0].caption = '{}\n\n<code>{}</code>'.format(post['text'], pub_name)
        message_payload['media'][0].parse_mode = 'HTML'
    else:
        return None
    return media_type, message_payload
