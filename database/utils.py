import time
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator

from database import Session


def timestamp_now() -> int:
    return int(time.mktime(datetime.utcnow().timetuple()))


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
