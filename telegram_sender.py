import os
import asyncio
from telegram import Bot, InputMediaPhoto
from settings import TELEGRAM_BOT_TOKEN, SUBSCRIBERS, NIGHT_MODE, NIGHT_RANGE
from datetime import datetime

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def is_night():
    if not NIGHT_MODE:
        return False
    hour = datetime.now().hour
    start, end = NIGHT_RANGE
    return start <= hour < end if start < end else (hour >= start or hour < end)

async def send_to_telegram(text, image_path=None):
    for chat_id in SUBSCRIBERS:
        try:
            if image_path and os.path.exists(image_path):
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=open(image_path, "rb"),
                    caption=text,
                    parse_mode="HTML",
                    disable_notification=is_night()
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode="HTML",
                    disable_notification=is_night()
                )
        except Exception as e:
            print(f"❌ Помилка відправки в Telegram: {e}")