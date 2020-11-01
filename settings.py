import os

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = bool(int(os.getenv('DEBUG', 1)))

# VK
VK_API_KEY = os.getenv('VK_API_KEY')

# TG
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_SEND_FRESH_POSTS_IN_EVERY_SECONDS = 60 * 30  # 30 min

# DB
DATABASE_URL = os.getenv('DATABASE_URL')
