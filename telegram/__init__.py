from decouple import config
from telethon import TelegramClient

BOT_TOKEN = config("BOT_TOKEN")
API_ID = config("TELEGRAM_API_ID")
API_HASH = config('TELEGRAM_API_HASH')
CLIENT = TelegramClient('session', API_ID, API_HASH)
DB_CHANNEL_ID = int(config('DB_CHANNEL_ID'))
BOT_ID = config('BOT_ID')
