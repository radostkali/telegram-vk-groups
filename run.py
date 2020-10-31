import os
import logging
from logging.handlers import RotatingFileHandler

from telegram_service.bot import TgBot
from database.services.tables_control_service import DBTablesControlService

import settings


if __name__ == '__main__':
    if settings.DEBUG:
        logging.basicConfig(
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.DEBUG,
        )
    else:
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

    db_tables_control_service = DBTablesControlService()
    db_tables_control_service.create_tables()

    bot = TgBot()
    bot.start()
