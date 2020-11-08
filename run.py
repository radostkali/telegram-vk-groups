import os
import logging
from logging.handlers import RotatingFileHandler

from telegram_service.bot import TgBot
from database.services.tables_control_service import DBTablesControlService
from database.daos.last_refresh_dao import LastRefreshDAO
from database.utils import db_session

import settings


if __name__ == '__main__':
    if settings.DEBUG:
        from datetime import datetime, timedelta
        with db_session() as session:
            last_refresh = LastRefreshDAO._get_or_create_last_refresh(session)
            last_refresh.timestamp = int(
                ((
                     datetime.utcnow() - timedelta(hours=5)
                 ) - datetime(1970, 1, 1)).total_seconds()
            )
        logging.basicConfig(
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.NOTSET,
        )
    else:
        log_filepath = os.path.join(settings.BASEDIR, 'logs', 'tg_bot.log')
        handler = RotatingFileHandler(
            filename=log_filepath,
            maxBytes=1024 * 1024 * 50,  # 50 mb
            backupCount=3,
        )
        logging.basicConfig(
            handlers=[handler],
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.DEBUG,
        )

    db_tables_control_service = DBTablesControlService()
    db_tables_control_service.create_tables()

    bot = TgBot()
    bot.start()
