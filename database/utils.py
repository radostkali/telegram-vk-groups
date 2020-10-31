from contextlib import contextmanager
from datetime import datetime
from typing import Iterator

from database import Session


def timestamp_now() -> int:
    return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())


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
