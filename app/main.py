import logging

from tg.bot import TgBot


bot = TgBot(loglevel=logging.DEBUG)
bot.start()
