from aiogram import Bot

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


async def send_alert(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    finally:
        await bot.session.close()
