import app.bot.handlers
import app.bot.handlers.messages

from app.bot.dependencies import dp, bot

async def start_bot():
    await dp.start_polling(bot)
