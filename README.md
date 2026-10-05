# Crypto Signal Bot

An asynchronous Python bot that monitors cryptocurrency markets and sends real-time Telegram alerts based on technical analysis signals.

Built as a learning project to practice asynchronous programming, exchange API integration, data analysis with pandas, and clean modular architecture — not as an automated trading system.

## What it does

- Fetches OHLCV (candlestick) data for BTC/USDT and ETH/USDT from Binance on a 15-minute timeframe, using concurrent async requests via `asyncio.gather`.
- Calculates RSI (Relative Strength Index) and SMA (Simple Moving Average) indicators with `pandas_ta`.
- Sends a Telegram alert when RSI drops below 30 (oversold) or rises above 70 (overbought).
- Runs continuously in a loop, re-checking the market every 15 minutes.

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| `asyncio` | Non-blocking, concurrent execution |
| `ccxt` (async) | Binance API integration |
| `pandas` / `pandas_ta` | Data manipulation and technical indicators |
| `aiogram` 3.x | Telegram bot notifications |
| `python-dotenv` | Environment variable / secrets management |

## Architecture

The project is split into single-responsibility modules rather than one large script:

```
crypto-signal-bot/
├── config.py              # loads .env and exposes settings to the rest of the app
├── data_fetcher.py        # fetches OHLCV data from Binance (async)
├── analytics.py           # calculates RSI/SMA and checks for signals
├── telegram_notifier.py   # sends alerts via Telegram
├── main.py                # orchestrates the above in a continuous loop
├── requirements.txt
└── .env.example           # template for required environment variables
```

Each module can be tested and understood independently. For example, swapping Binance for another exchange only requires changes in `data_fetcher.py` — nothing else in the codebase needs to know.

## Design decisions worth noting

- **Fail-fast configuration**: `config.py` raises an error immediately on startup if required settings (like the Telegram token) are missing, instead of letting the bot fail later with an unclear error.
- **Broad exception handling in the main loop**: unlike the strict, specific error handling used elsewhere (e.g. `FileNotFoundError`), the main loop in `main.py` deliberately catches any exception during a single check cycle, logs it, and continues — a long-running bot shouldn't crash permanently over one temporary network issue.
- **No trading, no withdrawal permissions**: the bot only reads public market data; no Binance API key is required for its current functionality.

## Setup

1. Clone the repository and move into it:
   ```
   git clone https://github.com/horabnatinov/crypto-signal-bot.git
   cd crypto-signal-bot
   ```

2. Create and activate a virtual environment (Python 3.10–3.13 recommended):
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your own values:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```
   A Telegram bot token can be created via [@BotFather](https://t.me/BotFather); your chat ID can be found by messaging your bot and checking `https://api.telegram.org/bot<TOKEN>/getUpdates`.

5. Run the bot:
   ```
   python main.py
   ```

## Example output

```
Отримуємо дані...
BTC/USDT: без сигналу
ETH/USDT: без сигналу
Чекаємо 900 секунд до наступної перевірки...
```

When RSI crosses a threshold, a message like this is sent to Telegram:

```
🟢 BTC/USDT: RSI = 28.43 — Перепроданість (oversold)
```

## Possible future improvements

- Support for more trading pairs and configurable timeframes
- Additional indicators (MACD, Bollinger Bands)
- A simple web dashboard showing current indicator values
- Persisting signal history to a database instead of only sending alerts
