from typing import Optional
from dataclasses import dataclass

from database.models import User
from database.utils import db_session


@dataclass
class UserDTO:
    user_id: int
    login: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserDAO:
    @classmethod
    def check_if_user_exists(cls, user_id: int) -> bool:
        with db_session() as session:
            user = session.query(
                User
            ).filter_by(
                id=user_id
            ).first()
        return bool(user)

    @classmethod
    def create_user(cls, user_dto: UserDTO) -> None:
        with db_session() as session:
            user = User(
                id=user_dto.user_id,
                login=user_dto.login,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
            )
            session.add(user)
