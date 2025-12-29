from app.dependencies import llm_engine
from app.database.base import init_db
from app.database import parse_and_save

import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    init_db()
    reply = llm_engine.completion("Скажи 'Hello, world!'")["reply"]
    print(reply)
    # parse_and_save()
