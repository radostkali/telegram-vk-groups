import time
import traceback

from database.daos.last_refresh_dao import LastRefreshDAO

from fetch_and_send_service.loggers import FetchAndSendBaseLogger
from fetch_and_send_service.services.fetch_fresh_posts_to_messages_service import FetchFreshPostsToMessagesService
from fetch_and_send_service.services.send_tg_message_service import SendTgMessageService


class FetchingAndSendingMaxLimitError(Exception):
    pass


class FetchAndSendFreshPostsUsecase:

    SEND_MESSAGES_MAX_TRY_COUNT = 3
    SLEEP_BETWEEN_MESSAGES_SENDING = 1
    SLEEP_BETWEEN_RETRIES = 5

    def __init__(
            self,
            fetch_fresh_posts_to_messages_service: FetchFreshPostsToMessagesService,
            send_tg_message_service: SendTgMessageService,
            logger: FetchAndSendBaseLogger,
    ) -> None:
        self.fetch_fresh_posts_to_messages_service = fetch_fresh_posts_to_messages_service
        self.send_tg_message_service = send_tg_message_service
        self.logger = logger

    def execute(self):
        last_refresh = LastRefreshDAO.get_last_refresh()
        for _ in range(self.SEND_MESSAGES_MAX_TRY_COUNT):
            message_dto = None
            try:
                messages_dto_list = self.fetch_fresh_posts_to_messages_service.execute(
                    from_timestamp=last_refresh
                )
                for message_dto in messages_dto_list:
                    self.send_tg_message_service.execute(message_dto=message_dto)
                    time.sleep(self.SLEEP_BETWEEN_MESSAGES_SENDING)
            except Exception:
                self.logger.log(traceback.format_exc())
                self.logger.log('message_dto: {}'.format(message_dto))
                time.sleep(self.SLEEP_BETWEEN_RETRIES)
                continue
            else:
                LastRefreshDAO.update_last_refresh()
                break
        else:
            self.logger.log('MAX FETCH AND SEND LIMIT COUNT EXCEED')
            raise FetchingAndSendingMaxLimitError
