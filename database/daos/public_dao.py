from dataclasses import dataclass

from database.models import Public
from database.utils import db_session


@dataclass
class PublicDTO:
    public_id: int
    public_name: str
    public_slug_url: str


class PublicDAO:

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
