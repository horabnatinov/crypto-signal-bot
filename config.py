import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SYMBOLS = os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT").split(",")
TIMEFRAME = os.getenv("TIMEFRAME", "15m")

RSI_PERIOD = int(os.getenv("RSI_PERIOD", 14))
RSI_OVERSOLD = int(os.getenv("RSI_OVERSOLD", 30))
RSI_OVERBOUGHT = int(os.getenv("RSI_OVERBOUGHT", 70))
SMA_PERIOD = int(os.getenv("SMA_PERIOD", 50))

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN і TELEGRAM_CHAT_ID мають бути задані в .env")
