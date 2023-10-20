from aiogram import Bot, Dispatcher
from app.handlers import router
import asyncio
import sqlite3
import os


async def prim():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    with sqlite3.connect("db.sqlite3") as database:
        database.cursor().execute("""
                                  CREATE TABLE
                                  IF NOT EXITS
                                  users(id INT, city TEXT);
                                  """)

    await dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(prim())
