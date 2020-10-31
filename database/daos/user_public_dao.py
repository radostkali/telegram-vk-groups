from typing import List
from dataclasses import dataclass

from database.utils import db_session
from database.daos.public_dao import PublicDTO

from database.models import User, Public, UserPublic


@dataclass
class UserPublicRefreshDTO:
    user_id: int
    publics: List[PublicDTO]


class UserPublicDAO:

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
    def get_user_publics(cls, user_id: int) -> List[PublicDTO]:
        with db_session() as session:
            user = session.query(User).get(user_id)
            publics_dto_list = [
                PublicDTO(
                    public_id=user_public.public.id,
                    public_name=user_public.public.name,
                    public_slug_url=user_public.public.slug_url,
                ) for user_public in user.publics
            ]
            return publics_dto_list

    @classmethod
    def remove_user_public(cls, user_id: int, public_id: int) -> None:
        with db_session() as session:
            user_public = session.query(
                UserPublic
            ).filter_by(
                user_id=user_id,
                public_id=public_id,
            ).first()
            session.delete(user_public)

            public = session.query(Public).get(public_id)
            if len(public.users) == 0:
                session.delete(public)

    @classmethod
    def get_users_publics_to_refresh(cls) -> List[UserPublicRefreshDTO]:
        with db_session() as session:
            users = session.query(User).all()
            user_public_refresh_dto_list = []
            for user in users:
                publics_dto_list = [
                    PublicDTO(
                        public_id=user_public.public.id,
                        public_name=user_public.public.name,
                        public_slug_url=user_public.public.slug_url,
                    ) for user_public in user.publics
                ]
                user_public_refresh_dto = UserPublicRefreshDTO(
                    user_id=user.id,
                    publics=publics_dto_list,
                )
                user_public_refresh_dto_list.append(user_public_refresh_dto)

        return user_public_refresh_dto_list
