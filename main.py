import logging

from aiogram import executor

from app.handlers import dp


async def on_startup(dp):
    from loader import cur, conn
    from app.utils.database import init_database
    from app.utils.commands import set_default_commands

    init_database(cur, conn)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s --> %(message)s")
    await set_default_commands(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
