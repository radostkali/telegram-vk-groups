from contextlib import contextmanager
from typing import Iterator, Dict, Union, List, Any, Optional
from datetime import datetime

from db.models import Base, User, Public, UserPublic
from db import engine, Session


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


class DBTablesControlService:
    def create_tables(self) -> None:
        Base.metadata.create_all(engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(engine)

    def recreate_tables(self) -> None:
        self.drop_tables()
        self.create_tables()


def check_if_user_exists(user_id: int) -> bool:
    with db_session() as s:
        user = s.query(User).filter_by(id=user_id).first()
    return False if not user else True


def put_user_in_db(
        user_id: int,
        login: str,
        first_name: Optional[str],
        last_name: Optional[str],
) -> None:
    with db_session() as s:
        timestamp_now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
        user = User(
            id=user_id,
            last_refresh=timestamp_now,
            login=login,
            first_name=first_name,
            last_name=last_name,
        )
        s.add(user)


def check_if_public_exists(public_id: int) -> bool:
    with db_session() as s:
        public = s.query(Public).filter_by(id=public_id).first()
    return False if not public else True


def put_public_in_db(public_info: Dict[str, Union[int, str]]) -> None:
    with db_session() as s:
        public = Public(
            id=public_info['public_id'],
            name=public_info['public_name'],
            slug_url=public_info['public_slug_url'],
        )
        s.add(public)


def link_public_to_user(user_id: int, public_id: int) -> None:
    with db_session() as s:
        if not s.query(UserPublic).filter_by(user_id=user_id, public_id=public_id).first():
            user = s.query(User).get(user_id)
            public = s.query(Public).get(public_id)
            user_public = UserPublic()
            user_public.public = public
            user_public.user = user
            public.users.append(user_public)
            user.publics.append(user_public)


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


if __name__ == '__main__':
    recreate_tables()
