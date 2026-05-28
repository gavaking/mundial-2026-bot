#!/usr/bin/env python3
"""
Bot handler - Risponde ai messaggi su Telegram
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Risponde a /start"""
    await update.message.reply_text(
        "👋 Ciao! Sono il bot Mondiale 2026!\n\n"
        "Riceverai notifiche sulle partite ogni giorno alle 08:30."
    )

async def main() -> None:
    """Avvia il bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    # Avvia il bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
