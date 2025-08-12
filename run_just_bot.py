# Bot_tel.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, Application, ContextTypes
from dev_func import start, handle_message, send_news_to_all_BTC   # ← اینو پایین می‌نویسم
import asyncio

class dev_pirate_crypto_nonenews:
    def __init__(self, Token: str):
        self.app: Application = (
            ApplicationBuilder()
            .token(Token)
            .build()
        )
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    def run(self):
        self.app.run_polling()
