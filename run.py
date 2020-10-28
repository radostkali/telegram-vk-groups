import logging

from tg.bot import TgBot
from db.crud import create_tables, drop_tables
import settings


if __name__ == '__main__':
    drop_tables()
    create_tables()

    loglevel = logging.DEBUG if settings.DEBUG else logging.CRITICAL

    bot = TgBot(loglevel=loglevel)
    bot.start()
