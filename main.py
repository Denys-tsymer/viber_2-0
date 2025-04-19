import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
from viber import send_message, send_photo
from PIL import Image
from pytesseract import image_to_string

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = "7584591858:AAGHg6ziy1pc5P7Ed1w8eM5-WlsCVMz4nAY"
SUBSCRIBERS = [
    7148393020,
    -1001632282594
]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help!")

def error(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()