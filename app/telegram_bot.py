import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.config import TELEGRAM_BOT_TOKEN
from app.storage import Storage

logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self):
        self.storage = Storage()

        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(CommandHandler("add", self.add_keyword))
        self.app.add_handler(CommandHandler("remove", self.remove_keyword))
        self.app.add_handler(CommandHandler("list", self.list_keywords))

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Bot activo")

    async def add_keyword(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.args:
            keyword = context.args[0]
            self.storage.add_keyword(keyword)
            await update.message.reply_text(f"➕ Añadido: {keyword}")
        else:
            await update.message.reply_text("Uso: /add palabra")

    async def remove_keyword(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.args:
            keyword = context.args[0]
            self.storage.remove_keyword(keyword)
            await update.message.reply_text(f"➖ Eliminado: {keyword}")
        else:
            await update.message.reply_text("Uso: /remove palabra")

    async def list_keywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keywords = self.storage.get_keywords()

        if keywords:
            text = "📌 Keywords activas:\n" + "\n".join(f"- {k}" for k in keywords)
        else:
            text = "No hay keywords configuradas"

        await update.message.reply_text(text)

    def run(self):
        logger.info("Telegram bot corriendo...")
        self.app.run_polling()