import logging
from aiogram.types import Message

from app.core.query_dispatcher import execute_analytics_query
from app.database.base import get_db
from app.dependencies import llm_engine
from app.bot.dependencies import dp
from app.schemas.llm import AnalyticsQuery
from app.utils.data_parser import parse_llm_response


def handle_user_message(text: str) -> str:
    llm_raw = llm_engine.completion(text or "").get("reply", "")
    payload = parse_llm_response(llm_raw)
    query = AnalyticsQuery.model_validate(payload)

    with get_db() as session:
        result = execute_analytics_query(session, query)

    return str(result or 0)

@dp.message()
async def echo(msg: Message):
    try:
        reply = handle_user_message(msg.text or "")
        await msg.reply(text=reply)
    except TypeError as e:
        logging.error(e)
        await msg.answer("Unknown error! See logs...")
