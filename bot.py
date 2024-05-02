import asyncio
import logging
import handlers
from aiogram import Bot, Dispatcher
from config_reader import config
from database.data import get_database

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    db = get_database()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

