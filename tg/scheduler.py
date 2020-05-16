import time

from telegram.ext import CallbackContext

from tg.utils import prepare_new_posts
from tg.msg_media_types import MESSAGE_MEDIA_TYPES


def get_posts(context):
    # type: (CallbackContext) -> None
    posts = prepare_new_posts()
    for post in posts:
        if post:
            MESSAGE_MEDIA_TYPES[post[0]](context, post[1])
            time.sleep(1)


SCHEDULERS = (
    # (callback, timeout)
    (get_posts, 180),
)

