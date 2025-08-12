# Bot_tel.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, Application, ContextTypes
from dev_func import start, handle_message, send_news_to_all   # ← اینو پایین می‌نویسم
import asyncio

class dev_pirate_crypto:
    def __init__(self, Token: str):
        self.app: Application = (
            ApplicationBuilder()
            .token(Token)
            .post_init(self._on_post_init)  # بعد از build اجرا میشه
            .build()
        )
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    async def _on_post_init(self, app: Application):
        # یک تسک پس‌زمینه‌ای؛ کوچیک هم مکث کنه تا بات کامل بالا بیاد
        app.create_task(self._startup_task(app))

    async def _startup_task(self, app: Application):
        await asyncio.sleep(1)
        await send_news_to_all(app.bot)  # ← بدون نیاز به JobQueue

    def run(self):
        self.app.run_polling()
