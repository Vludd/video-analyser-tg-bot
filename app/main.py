from app.bot.client import start_bot
from app.dependencies import llm_engine
from app.database.base import init_db
from app.database import parse_and_save

import asyncio

import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def start():
    init_db()
    # parse_and_save()
    await start_bot()
    

if __name__ == "__main__":
    asyncio.run(start())