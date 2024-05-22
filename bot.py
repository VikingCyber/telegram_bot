import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from pymongo.database import Database

from config_reader import config
from database import get_database
from dao import PlayerDao
from game import GuessGame
from models import Player

logging.basicConfig(level=logging.INFO)


bot: Bot = Bot(token=config.bot_token.get_secret_value())
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def start_handler(message: Message):
    await message.answer(f"Привет, {message.chat.first_name}! Этот бот поможет тебе узнать чуточку больше об истории"
                         f" страны в игровой форме. Для того чтобы узнать правила игры и "
                         f"список доступных команд введи /help.  ")
    player = Player(_id=message.from_user.id)
    player = players.create(player)


@dp.message(Command(commands=['help']))
async def help_handler(message: Message):
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
                         f"Для начала игры введите /play")


@dp.message(Command(commands=['play']))
async def play_handler(message: Message):
    event = game.play(message.from_user.id)
    await message.answer(event.event)


@dp.message(Command(commands=['sur']))
async def sur_handler(message: Message):
    player = game.get_player(message.from_user.id)
    if not player.in_game:
        await message.answer('Вы сейчас не в игре. Для начала игры введите /play')
    else:
        event = game.surrender(player)
        await message.answer(event.explain())
        if image := event.get_image_file():
            await message.answer_photo(image)
        if event.description:
            await message.answer(event.description)


@dp.message(lambda x: x.text and x.text.isdigit())
async def data_answer_handler(message: Message):
    date = int(message.text)
    player = game.get_player(message.from_user.id)

    if not player.in_game:
        await message.answer("Вы сейчас не в игре. Для начала игры введите /play")
    elif not 0 <= date <= 2024:
        await message.answer('Временные рамки от 0 до 2024 года.')
    else:
        msg, event = game.guess(player, date)
        if event:
            await message.answer(event.explain())
            if image := event.get_image_file():
                await message.answer_photo(image)
            if event.description:
                await message.answer(event.description)
        else:
            await message.answer(msg)


@dp.message(Command(commands=['stats']))
async def stat_handler(message: Message):
    player = game.get_player(message.from_user.id)
    guessed_events_amount = len(player.guessed_events)
    try:
        attempts_average = round(player.attempts / guessed_events_amount)
    except ZeroDivisionError:
        attempts_average = 0
    await message.answer(
        f"Очки: {player.score}\n"
        f"Общее число попыток: {player.attempts}\n"
        f"Угаданных дат: {guessed_events_amount}\n"
        f"Среднее кол-во попыток на ответ: {attempts_average}"
    )


@dp.message(Command(commands=['cancel']))
async def cancel_handler(message: Message):
    player = game.get_player(message.from_user.id)
    if not player.in_game:
        await message.answer("Вы сейчас не в игре. Для начала игры введите /play")
    else:
        game.cancel(player)
        await message.answer('Вы вышли из игры, хотите сыграть снова? Введите /play')


@dp.message()
async def other_text_handler(message: Message):
    player = game.get_player(message.from_user.id)
    if player.in_game:
        await message.answer('Вы находитесь в игре, попробуйте угадать дату или сдавайтесь! /sur')
    else:
        await message.answer("Такой команды нет, введите /help для получения списка команд.")

if __name__ == "__main__":
    database: Database = get_database()
    players: PlayerDao = PlayerDao(database)
    with GuessGame(database) as game:
        dp.run_polling(bot)
