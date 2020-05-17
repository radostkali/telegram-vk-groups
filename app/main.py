import logging

from tg.bot import TgBot
from db.crud import create_tables
import settings


if __name__ == '__main__':
    create_tables()

    loglevel = logging.DEBUG if settings.DEBUG else logging.CRITICAL

    bot = TgBot(loglevel=loglevel)
    bot.start()
