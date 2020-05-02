from contextlib import contextmanager
from typing import Iterator, Dict, Union
from datetime import datetime

from db.models import Base, User, Public, UserPublic
from db import engine, Session


@contextmanager
def db_session():
    # type: () -> Iterator[Session]
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    # type: () -> None
    Base.metadata.create_all(engine)


def drop_tables():
    # type: () -> None
    Base.metadata.drop_all(engine)


def recreate_tables():
    # type: () -> None
    drop_tables()
    create_tables()


def check_if_user_exists(user_id):
    # type: (int) -> bool
    with db_session() as s:
        user = s.query(User).filter_by(id=user_id).first()
    return False if not user else True


def put_user_in_db(user_id):
    # type: (int) -> None
    with db_session() as s:
        user = User(id=user_id)
        s.add(user)


def check_if_public_exists(public_id):
    # type: (int) -> bool
    with db_session() as s:
        public = s.query(Public).filter_by(id=public_id).first()
    return False if not public else True


def put_public_in_db(public_info):
    # type: (Dict[str, Union[int, str]]) -> None
    with db_session() as s:
        public = Public(
            id=public_info['public_id'],
            public_name=public_info['public_name'],
            last_post=datetime(2000, 1, 1, 0, 0, 0),
            last_check=datetime(2000, 1, 1, 0, 0, 0),
        )
        s.add(public)


def link_public_to_user(user_id, public_id):
    # type: (int, int) -> None
    with db_session() as s:
        if not s.query(UserPublic).filter_by(user_id=user_id, public_id=public_id).first():
            user = s.query(User).get(user_id)
            public = s.query(Public).get(public_id)
            user_public = UserPublic(timestamp=datetime.utcnow())
            user_public.public = public
            user_public.user = user
            public.users.append(user_public)
            user.publics.append(user_public)


if __name__ == '__main__':
    recreate_tables()
