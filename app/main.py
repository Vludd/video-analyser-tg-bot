from app.bot.client import start_bot

import asyncio

import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def start():
    await start_bot()

if __name__ == "__main__":
    asyncio.run(start())
