from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "press to start"),
            types.BotCommand("add", "add task"),
            types.BotCommand("list", "list all tasks"),
            types.BotCommand("delete", "delete task"),
            types.BotCommand("complete", "complete task"),
            types.BotCommand("help", "help"),
        ]
    )
