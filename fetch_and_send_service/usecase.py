import time

from database.daos.last_refresh_dao import LastRefreshDAO

from fetch_and_send_service.services.fetch_fresh_posts_to_messages_service import FetchFreshPostsToMessagesService
from fetch_and_send_service.services.send_tg_message_service import SendTgMessageService


class FetchingAndSendingError(Exception):
    pass


class FetchAndSendFreshPostsUsecase:

    SEND_MESSAGES_MAX_TRY_COUNT = 3
    SLEEP_BETWEEN_MESSAGES_SENDING = 1

    def __init__(
            self,
            fetch_fresh_posts_to_messages_service: FetchFreshPostsToMessagesService,
            send_tg_message_service: SendTgMessageService,
    ) -> None:
        self.fetch_fresh_posts_to_messages_service = fetch_fresh_posts_to_messages_service
        self.send_tg_message_service = send_tg_message_service

    def execute(self):
        last_refresh = LastRefreshDAO.get_last_refresh()
        for _ in range(self.SEND_MESSAGES_MAX_TRY_COUNT):
            try:
                messages_dto_list = self.fetch_fresh_posts_to_messages_service.execute(
                    from_timestamp=last_refresh
                )
                for message_dto in messages_dto_list:
                    self.send_tg_message_service.execute(message_dto=message_dto)
                    time.sleep(self.SLEEP_BETWEEN_MESSAGES_SENDING)
            except Exception as e:
                continue
            else:
                LastRefreshDAO.update_last_refresh()
                break
        else:
            raise FetchingAndSendingError
