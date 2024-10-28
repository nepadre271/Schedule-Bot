import os
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_API_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
DIRECTIONS_GROUPS = os.getenv("DIRECTIONS_GROUPS").split(';')
DIRECTIONS = [item.split(':')[0] for item in DIRECTIONS_GROUPS]
GROUPS = {item.split(':')[0]: item.split(':')[1].split(',') for item in DIRECTIONS_GROUPS}

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
