from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.config import Config
from bot.main import create_bot, dp
import asyncio
from threading import Thread
import os

app = create_app()

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=True
    )
