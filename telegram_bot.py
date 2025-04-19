import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from settings import TELEGRAM_BOT_TOKEN

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот активний! Введіть /info для списку команд.")

# Команда /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
📋 Доступні команди:
/start — Запустити бота
/info — Показати список команд
/debug — Показати лог
/report — Статистика за день
/top — Топ-10 міст
/night_on — Ввімкнути нічний режим
/night_off — Вимкнути нічний режим
/set_night HH-HH — Задати нічний режим (напр. /set_night 00-06)
"""
    await update.message.reply_text(commands)

# Запуск бота
if __name__ == "__main__":
    print("✅ Telegram бот запускається...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Обробники команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))

    print("🤖 Бот слухає повідомлення...")
    app.run_polling()
