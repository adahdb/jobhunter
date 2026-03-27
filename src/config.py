import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#print(TELEGRAM_TOKEN)

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
#print(TELEGRAM_CHAT_ID)

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing!")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID is missing!")