from typing import List

from database.daos.user_public_dao import UserPublicDAO, UserPublicRefreshDTO
from vk_service import VkAPI

from fetch_and_send_service.services.vk_post_to_tg_message_service import VkPostToTgMessageService, TgMessageDTO


class FetchFreshPostsToMessagesService:

    def __init__(self, vk_post_to_tg_message_service: VkPostToTgMessageService) -> None:
        self.vk_post_to_tg_message_service = vk_post_to_tg_message_service

    def _prepare_messages_to_send(
            self,
            user_publics_refresh_dto_list: List[UserPublicRefreshDTO],
            from_timestamp: int,
    ) -> List[TgMessageDTO]:
        messages_to_send = []
        public_id_posts_dto_map = {}
        for user_publics_refresh_dto in user_publics_refresh_dto_list:
            for public_dto in user_publics_refresh_dto.publics:
                if public_dto.public_id not in public_id_posts_dto_map:
                    post_dto_list = VkAPI.fetch_fresh_posts(
                        public_id=public_dto.public_id,
                        from_timestamp=from_timestamp,
                    )
                    public_id_posts_dto_map[public_dto.public_id] = post_dto_list

                posts_dto_list = public_id_posts_dto_map[public_dto.public_id]
                for post_dto in posts_dto_list:
                    post_message_to_send = self.vk_post_to_tg_message_service.execute(
                        post=post_dto,
                        user_id=user_publics_refresh_dto.user_id,
                        public_id=public_dto.public_id,
                        public_name=public_dto.public_name,
                        public_slug=public_dto.public_slug_url,
                    )
                    if post_message_to_send.media_type:
                        messages_to_send.append(post_message_to_send)

        return messages_to_send

    def execute(self, from_timestamp: int) -> List[TgMessageDTO]:
        user_publics_refresh_dto_list = UserPublicDAO.get_users_publics_to_refresh()
        messages_to_send = self._prepare_messages_to_send(
            user_publics_refresh_dto_list=user_publics_refresh_dto_list,
            from_timestamp=from_timestamp,
        )
        return messages_to_send
