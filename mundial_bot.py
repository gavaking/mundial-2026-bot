#!/usr/bin/env python3
"""
Telegram Bot per seguire le partite del Mondiale 2026
"""

import requests
import os
from datetime import datetime
import pytz
from telegram import Bot
from telegram.error import TelegramError

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TIMEZONE = 'CET'

def get_matches_today():
    """Fetch matches for today"""
    try:
        today = datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d')
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_match_message(matches):
    """Format matches"""
    if not matches:
        return "⚽ Nessuna partita in programma oggi per il Mondiale 2026"
    
    message = "⚽ **PARTITE MONDIALE 2026 - OGGI**\n\n"
    return message

def send_telegram_message(text):
    """Send message to Telegram"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode='Markdown'
        )
        print(f"✅ Message sent successfully at {datetime.now()}")
        return True
    except TelegramError as e:
        print(f"❌ Telegram Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print(f"🤖 Starting Mondiale 2026 Bot at {datetime.now()}")
    
    matches = get_matches_today()
    message = format_match_message(matches)
    success = send_telegram_message(message)
    
    if success:
        print("✅ Bot execution completed successfully")
    else:
        print("❌ Bot execution failed")

if __name__ == '__main__':
    main()
