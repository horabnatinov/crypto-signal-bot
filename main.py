import asyncio

from data_fetcher import fetch_all_symbols
from analytics import calculate_indicators, check_signal
from telegram_notifier import send_alert


async def run_once():
    print("Fetching data...")
    data = await fetch_all_symbols()

    for symbol, df in data.items():
        df_with_indicators = calculate_indicators(df)
        signal = check_signal(df_with_indicators, symbol)

        if signal:
            print(f"Signal found: {signal}")
            await send_alert(signal)
        else:
            print(f"{symbol}: no signal")


async def main_loop(interval_seconds=900):
    while True:
        try:
            await run_once()
        except Exception as e:
            print(f"Error during check: {e}")

        print(f"Waiting {interval_seconds} seconds until next check...")
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(main_loop())
