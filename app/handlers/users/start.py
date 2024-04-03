from aiogram import types

from loader import dp


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Welcome to the To-Do List Manager! Use /add to add a task, /delete to delete a task, "
                        "/complete to mark a task as completed, /list to view your tasks, and /help for assistance.")
