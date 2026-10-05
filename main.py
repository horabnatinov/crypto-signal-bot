import asyncio

from data_fetcher import fetch_all_symbols
from analytics import calculate_indicators, check_signal
from telegram_notifier import send_alert


async def run_once():
    print("Отримуємо дані...")
    data = await fetch_all_symbols()

    for symbol, df in data.items():
        df_with_indicators = calculate_indicators(df)
        signal = check_signal(df_with_indicators, symbol)

        if signal:
            print(f"Сигнал знайдено: {signal}")
            await send_alert(signal)
        else:
            print(f"{symbol}: без сигналу")


async def main_loop(interval_seconds=900):
    while True:
        try:
            await run_once()
        except Exception as e:
            print(f"Помилка під час перевірки: {e}")

        print(f"Чекаємо {interval_seconds} секунд до наступної перевірки...")
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(main_loop())
