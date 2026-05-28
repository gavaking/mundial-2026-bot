#!/usr/bin/env python3
"""
Telegram Bot per seguire le partite del Mondiale 2026
Invia notifiche giornaliere con partite, pronostici e infortuni
"""

import requests
import os
from datetime import datetime
import pytz
from telegram import Bot
from telegram.error import TelegramError
import asyncio

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TIMEZONE = 'CET'

# API Configuration
API_KEY = os.getenv('API_FOOTBALL_KEY', '')
FOOTBALL_API_BASE = "https://api.api-football.com/v3"

async def get_matches_today():
    """Fetch matches for today from API"""
    try:
        today = datetime.now(pytz.timezone(TIMEZONE)).strftime('%Y-%m-%d')
        
        headers = {
            'x-rapidapi-host': 'api-football-beta.p.rapidapi.com',
            'x-rapidapi-key': API_KEY
        } if API_KEY else {}
        
        url = f"{FOOTBALL_API_BASE}/fixtures"
        params = {
            'date': today,
            'league': 1,
            'season': 2026
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get('response', [])
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching matches: {e}")
        return []

def format_match_message(matches):
    """Format matches into a readable Telegram message"""
    if not matches:
        return "⚽ Nessuna partita in programma oggi per il Mondiale 2026"
    
    message = "⚽ **PARTITE MONDIALE 2026 - OGGI**\n\n"
    
    for match in matches:
        fixture = match.get('fixture', {})
        teams = match.get('teams', {})
        
        date_str = fixture.get('date', 'N/A')
        time_str = date_str.split('T')[1][:5] if 'T' in date_str else 'N/A'
        
        home_team = teams.get('home', {}).get('name', 'Team A')
        away_team = teams.get('away', {}).get('name', 'Team B')
        
        status = fixture.get('status', 'NS')
        
        if status == 'NS':
            message += f"🕐 {time_str}\n"
        elif status in ['1H', '2H', 'HT']:
            message += f"🔴 LIVE\n"
        elif status == 'FT':
            message += f"✅ FINITA\n"
        
        score = match.get('score', {})
        goals_home = score.get('fulltime', {}).get('home')
        goals_away = score.get('fulltime', {}).get('away')
        
        if goals_home is not None and goals_away is not None:
            message += f"{home_team} {goals_home} - {goals_away} {away_team}\n\n"
        else:
            message += f"{home_team} vs {away_team}\n\n"
    
    message += f"\n📅 *Data*: {datetime.now(pytz.timezone(TIMEZONE)).strftime('%d/%m/%Y')}"
    
    return message

async def send_telegram_message(text):
    """Send message to Telegram chat"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(
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

async def main():
    """Main function"""
    print(f"🤖 Starting Mondiale 2026 Bot at {datetime.now()}")
    
    matches = get_matches_today()
    message = format_match_message(matches)
    success = await send_telegram_message(message)
    
    if success:
        print("✅ Bot execution completed successfully")
    else:
        print("❌ Bot execution failed")

if __name__ == '__main__':
    asyncio.run(main())
