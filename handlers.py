from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()  # [1]


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.chat.first_name}! Этот бот поможет тебе узнать чуточку больше об истории"
                         f" страны в игровой форме. Для того чтобы узнать правила игры и "
                         f"список доступных команд введи /help.  ")


@router.message(Command(commands=['help']))
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
