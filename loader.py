import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect('todo.db', check_same_thread=False)
cur = conn.cursor()

__all__ = ["bot", "dp", "conn", "cur"]
