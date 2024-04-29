from aiogram import types

from loader import dp


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    help_text = """
    Available commands:\n
    /add - Add a new task\n
    /delete - Delete a task\n
    /complete - Mark a task as completed\n
    /list - List all tasks\n
    /help - Show this help message
    """
    await message.reply(help_text)
