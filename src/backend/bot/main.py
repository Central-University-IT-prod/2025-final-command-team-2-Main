from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums.chat_type import ChatType

TOKEN = getenv("BOT_TOKEN")
WEBAPP_URL = getenv("WEBAPP_URL")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    webapp_button = InlineKeyboardButton(
        text="Открыть", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[webapp_button]])
    
    user_name = html.quote(message.from_user.full_name)
    
    if message.chat.type == ChatType.PRIVATE:
        greeting = f"<strong>Добро пожаловать, {user_name}!</strong> 👋\n\n"
    else:
        greeting = f"<strong>Привет всем в группе!</strong> 👋\n\n"
    
    await message.answer(
        greeting +
        "С помощью этого бота вы сможете:\n"
        "📌 Создавать коллекции фильмов\n"
        "📌 Находить фильмы по любимым цитатам\n" 
        "📌 Подбирать идеальный фильм для компании\n"
        "И это только начало! 🎬",
        reply_markup=keyboard
    )

def create_bot() -> Bot:
    return Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
