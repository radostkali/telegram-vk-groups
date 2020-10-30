import os
import logging
from logging.handlers import RotatingFileHandler

from tg.bot import TgBot
from db.db_tables_control_service import DBTablesControlService

import settings


if __name__ == '__main__':
    db_tables_control_service = DBTablesControlService()
    if settings.DEBUG:
        db_tables_control_service.recreate_tables()
        logging.basicConfig(
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.DEBUG,
        )
    else:
        db_tables_control_service.create_tables()
        log_filepath = os.path.join(settings.BASEDIR, 'logs', 'tg_bot.log')
        handler = RotatingFileHandler(
            filename=log_filepath,
            maxBytes=1024 * 1024 * 50,  # 50 mb
            backupCount=3,
        )
        logging.basicConfig(
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.CRITICAL,
        )

    bot = TgBot()
    bot.start()
