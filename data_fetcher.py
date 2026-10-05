import asyncio
import pandas as pd
import ccxt.async_support as ccxt

from config import SYMBOLS, TIMEFRAME


async def fetch_ohlcv(exchange, symbol, timeframe, limit=100):
    raw_data = await exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(
        raw_data,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["symbol"] = symbol

    return df


async def fetch_all_symbols(timeframe=TIMEFRAME, limit=100):
    exchange = ccxt.binance()

    try:
        tasks = [fetch_ohlcv(exchange, symbol, timeframe, limit) for symbol in SYMBOLS]
        results = await asyncio.gather(*tasks)
    finally:
        await exchange.close()

    return dict(zip(SYMBOLS, results))


if __name__ == "__main__":
    data = asyncio.run(fetch_all_symbols())

    for symbol, df in data.items():
        print(f"\n{symbol}:")
        print(df.tail(3))
