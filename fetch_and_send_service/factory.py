from telegram.ext import CallbackContext

from fetch_and_send_service.loggers import FetchAndSendDebugLogger, FetchAndSendErrorLogger
from fetch_and_send_service.services.fetch_fresh_posts_to_messages_service import FetchFreshPostsToMessagesService
from fetch_and_send_service.services.send_tg_message_service import SendTgMessageService
from fetch_and_send_service.services.vk_post_to_tg_message_service import VkPostToTgMessageService
from fetch_and_send_service.usecase import FetchAndSendFreshPostsUsecase

import settings


def fetch_and_send_fresh_posts_usecase_factory(callback_context: CallbackContext) -> FetchAndSendFreshPostsUsecase:
    vk_post_to_tg_message_service = VkPostToTgMessageService()
    fetch_fresh_posts_to_messages_service = FetchFreshPostsToMessagesService(
        vk_post_to_tg_message_service=vk_post_to_tg_message_service
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
