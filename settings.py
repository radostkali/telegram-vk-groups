import os
from dotenv import load_dotenv


load_dotenv()

# VK
VK_API_KEY = os.getenv('VK_API_KEY')
VK_API_VERSION = '5.103'

# TG
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

# DB
POSTGRES_URI = os.getenv('POSTGRES_URI')
