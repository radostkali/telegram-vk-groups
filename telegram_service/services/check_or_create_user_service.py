from database.daos.user_dao import UserDAO, UserDTO


class CheckOrCreateUserService:
    def execute(self, user_dto: UserDTO) -> None:
        user = UserDAO.check_if_user_exists(
            user_id=user_dto.user_id
        )
        if not user:
            UserDAO.create_user(user_dto=user_dto)
