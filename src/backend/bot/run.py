import asyncio
import logging
from dotenv import load_dotenv

from main import create_bot, dp

load_dotenv()

async def main() -> None:
    bot = create_bot()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
