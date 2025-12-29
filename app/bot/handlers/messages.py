import logging
from aiogram.types import Message

from app.dependencies import llm_engine
from app.bot.dependencies import dp

@dp.message()
async def echo(msg: Message):
    try:
        reply = llm_engine.completion(msg.text or "")
        
        reply_text = reply.get("reply", "")
        if reply_text:
            await msg.reply(text=reply_text)
    except TypeError as e:
        logging.error(e)
        await msg.answer("Unknown error! See logs...")
