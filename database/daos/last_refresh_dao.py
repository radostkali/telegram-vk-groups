from database import Session
from database.models import LastRefresh
from database.utils import timestamp_now, db_session


class LastRefreshDAO:
    @classmethod
    def _get_or_create_last_refresh(cls, session: Session):
        instance = session.query(LastRefresh).first()
        if instance:
            return instance
        else:
            instance = LastRefresh(
                id=1,
                timestamp=timestamp_now()
            )
            session.add(instance)
        return instance

    @classmethod
    def update_last_refresh(cls) -> None:
        with db_session() as session:
            last_refresh = cls._get_or_create_last_refresh(session)
            last_refresh.timestamp = timestamp_now()

    @classmethod
    def get_last_refresh(cls) -> int:
        with db_session() as session:
            last_refresh = cls._get_or_create_last_refresh(session)
            last_refresh_timestamp = last_refresh.timestamp
        return last_refresh_timestamp
