from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.dependencies import dp

@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer("Привет! Я тестовый бот Video Analyzer! Напиши свой запрос")
