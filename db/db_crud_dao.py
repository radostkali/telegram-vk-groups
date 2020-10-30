from contextlib import contextmanager
from typing import Iterator, Dict, Union, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from vk.api import PublicDTO
from db.models import User, Public, UserPublic
from db import Session


@contextmanager
def db_session() -> Iterator[Session]:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@dataclass
class UserPublicRefreshDTO:
    user_id: int
    last_refresh: int
    publics: List[PublicDTO]


class DBCrudDAO:

    @staticmethod
    def timestamp_now() -> int:
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())

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
    def create_user(
            cls,
            user_id: int,
            login: str,
            first_name: Optional[str],
            last_name: Optional[str],
    ) -> None:
        with db_session() as session:
            user = User(
                id=user_id,
                last_refresh=cls.timestamp_now(),
                login=login,
                first_name=first_name,
                last_name=last_name,
            )
            session.add(user)

    @classmethod
    def check_if_public_exists(cls, public_id: int) -> bool:
        with db_session() as session:
            public = session.query(
                Public
            ).filter_by(
                id=public_id
            ).first()
        return bool(public)

    @classmethod
    def create_public(cls, public_dto: PublicDTO) -> None:
        with db_session() as session:
            public = Public(
                id=public_dto.public_id,
                name=public_dto.public_name,
                slug_url=public_dto.public_slug_url,
            )
            session.add(public)

    @classmethod
    def link_public_to_user(cls, user_id: int, public_id: int) -> None:
        with db_session() as session:
            user_public_relation = session.query(
                UserPublic
            ).filter_by(
                user_id=user_id,
                public_id=public_id
            ).first()
            if not user_public_relation:
                user = session.query(User).get(user_id)
                public = session.query(Public).get(public_id)
                user_public = UserPublic()
                user_public.public = public
                user_public.user = user
                public.users.append(user_public)
                user.publics.append(user_public)

    @classmethod
    def get_users_publics_to_refresh(cls) -> List[UserPublicRefreshDTO]:
        with db_session() as session:
            users = session.query(User).all()
            user_public_refresh_dto_list = []
            for user in users:
                publics = [
                    PublicDTO(
                        public_id=public.id,
                        public_name=public.name,
                        public_slug_url=public.slug_url,
                    ) for public in user.publics
                ]
                user_public_refresh_dto = UserPublicRefreshDTO(
                    user_id=user.id,
                    last_refresh=user.last_refresh,
                    publics=publics,
                )
                user_public_refresh_dto_list.append(user_public_refresh_dto)

            return user_public_refresh_dto_list

    @classmethod
    def update_user_last_refresh(cls, user_id: int) -> None:
        with db_session() as session:
            user = session.query(User).get(user_id)
            user.last_refresh = cls.timestamp_now()


def get_users_publics_to_refresh() -> Dict[int, Dict[str, Union[str, Dict[int, Dict[str, Union[str, List[Any]]]]]]]:
    with db_session() as s:
        users = s.query(User).all()
        users_dict = {}
        for user in users:
            user_id = user.id
            last_refresh = user.last_refresh
            publics = user.publics
            users_dict[user_id] = {
                'last_refresh': last_refresh,
                'publics': {
                    i.public.id:
                        {
                            'name': i.public.name,
                            'posts': [],
                        } for i in publics
                }
            }
        return users_dict


def update_user_last_refresh(user_id: int) -> None:
    with db_session() as s:
        user = s.query(User).get(user_id)
        timestamp_now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
        user.last_refresh = timestamp_now


def get_user_publics(user_id: int) -> Dict[int, str]:
    with db_session() as s:
        user = s.query(User).get(user_id)
        publics = {p.public.id: p.public.name for p in user.publics}
        return publics


def remove_user_public_by_id(user_id: int, public_id: int) -> bool:
    with db_session() as s:
        user_public = s.query(UserPublic).filter_by(
            user_id=user_id,
            public_id=public_id,
        ).first()
        s.delete(user_public)
        public = s.query(Public).get(public_id)
        if len(public.users) == 0:
            s.delete(public)
        return True
