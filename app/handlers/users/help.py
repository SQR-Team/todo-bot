from aiogram import types

from loader import dp


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = """
    Available commands:
    /add - Add a new task
    /delete - Delete a task
    /complete - Mark a task as completed
    /list - List all tasks
    /help - Show this help message
    """
    await message.reply(help_text)
