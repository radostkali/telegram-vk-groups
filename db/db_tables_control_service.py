from db import engine
from db.models import Base


class DBTablesControlService:
    def create_tables(self) -> None:
        Base.metadata.create_all(engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(engine)

    def recreate_tables(self) -> None:
        self.drop_tables()
        self.create_tables()
