from telegram.ext import CallbackContext

from vk_service.services import VkFetchFreshPostsService

from fetch_and_send_service.loggers import (
    FetchAndSendDebugLogger,
    FetchAndSendErrorLogger,
)
from fetch_and_send_service.services import (
    FetchFreshPostsToMessagesService,
    SendTgMessageService,
    VkPostToTgMessageService,
)
from fetch_and_send_service.usecase import FetchAndSendFreshPostsUsecase

import settings


def fetch_and_send_fresh_posts_usecase_factory(callback_context: CallbackContext) -> FetchAndSendFreshPostsUsecase:
    vk_post_to_tg_message_service = VkPostToTgMessageService()
    vk_fetch_fresh_posts_service = VkFetchFreshPostsService()
    fetch_fresh_posts_to_messages_service = FetchFreshPostsToMessagesService(
        vk_post_to_tg_message_service=vk_post_to_tg_message_service,
        vk_fetch_fresh_posts_service=vk_fetch_fresh_posts_service,
    )
    send_tg_message_service = SendTgMessageService(
        callback_context=callback_context
    )
    logger = FetchAndSendDebugLogger() if settings.DEBUG else FetchAndSendErrorLogger()
    usecase = FetchAndSendFreshPostsUsecase(
        fetch_fresh_posts_to_messages_service=fetch_fresh_posts_to_messages_service,
        send_tg_message_service=send_tg_message_service,
        logger=logger,
    )
    return usecase
