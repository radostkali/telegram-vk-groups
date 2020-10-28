import logging

from tg.bot import TgBot
from db.crud import DBTablesControlService
import settings


if __name__ == '__main__':
    db_tables_control_service = DBTablesControlService()
    if settings.DEBUG:
        db_tables_control_service.recreate_tables()
        loglevel = logging.DEBUG
    else:
        db_tables_control_service.create_tables()
        loglevel = logging.CRITICAL

    bot = TgBot(loglevel=loglevel)
    bot.start()
