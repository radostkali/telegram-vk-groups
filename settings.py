import os

DEBUG = True if int(os.getenv('DEBUG')) == 1 else False

# VK
VK_API_KEY = os.getenv('VK_API_KEY')
VK_API_VERSION = '5.103'

# TG
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
HEROKU_PORT = os.environ.get('PORT')
HEROKU_APP_NAME = 'tg-bot-vk-aggregator'

# DB
DATABASE_URL = os.getenv('DATABASE_URL')
