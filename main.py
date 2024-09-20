import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from dotenv import load_dotenv

from app.database.models import db_main

from app.handlers.start import router_start
from app.handlers.calculation import router_calculation
from app.handlers.profile import router_profile
from app.handlers.support import router_support


async def main():
    await db_main()

    load_dotenv()

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(
        router_start,
        router_calculation,
        router_profile,
        router_support
    )
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
