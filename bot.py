import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from pymongo.database import Database

from config_reader import config
from database import get_database
from dao import PlayerDao

logging.basicConfig(level=logging.INFO)


# async def main():
#     bot = Bot(token=config.bot_token.get_secret_value())
#     dp = Dispatcher()
#     history_dao = HistoricalEventDao(db_obj)
#     dp.include_routers(handlers.router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
#
# if __name__ == '__main__':
#     db_obj = get_database()
#     asyncio.run(main())


bot: Bot = Bot(token=config.bot_token.get_secret_value())
dp: Dispatcher = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.chat.first_name}! Этот бот поможет тебе узнать чуточку больше об истории"
                         f" страны в игровой форме. Для того чтобы узнать правила игры и "
                         f"список доступных команд введи /help.  ")
    player = Player(_id=message.from_user.id)
    player = Player.create(player)


@dp.message(Command(commands=['help']))
async def help_handler(message: Message) -> None:
    await message.answer(f"Правила игры: \nБот называет вам историческое событие из истории России, "
                         f" вам нужно отгадать в каком году оно произошло. У вас есть 5 попыток. В независимости от"
                         f" исхода игры бот выведет краткую историческую справку о событии.\n"
                         f"Пример: \n"
                         f"Дата отмены крепостного права? \n"
                         f"Ответ: 1861\n"
                         f"Список доступных команд:\n"
                         f"/help - список команд и правила игры\n"
                         f"/play - начать игру\n"
                         f"/sur - сдаться\n"
                         f"/cancel - отменить игру\n"
                         f"/stats - посмотреть статистику\n"
                         f"Для начала игры введите /play!")


if __name__ == "__main__":
    database: Database = get_database()
    players: PlayerDao = PlayerDao(database)
