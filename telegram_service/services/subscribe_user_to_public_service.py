from database.daos.user_public_dao import UserPublicDAO
from database.daos.public_dao import PublicDAO, PublicDTO


class SubscribeUserToPublicService:
    def execute(self, user_id: int, public_dto: PublicDTO) -> None:
        public = PublicDAO.check_if_public_exists(
            public_id=public_dto.public_id
        )
        if not public:
            PublicDAO.create_public(public_dto=public_dto)

        UserPublicDAO.link_public_to_user(
            user_id=user_id,
            public_id=public_dto.public_id,
        )
