import pandas as pd
import pandas_ta as ta

from config import RSI_PERIOD, SMA_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT


def calculate_indicators(df):
    df = df.copy()
    df["rsi"] = ta.rsi(df["close"], length=RSI_PERIOD)
    df["sma"] = ta.sma(df["close"], length=SMA_PERIOD)
    return df


def check_signal(df, symbol):
    last_row = df.iloc[-1]
    rsi_value = last_row["rsi"]

    if pd.isna(rsi_value):
        return None

    if rsi_value < RSI_OVERSOLD:
        return f"🟢 {symbol}: RSI = {rsi_value:.2f} — Oversold"
    elif rsi_value > RSI_OVERBOUGHT:
        return f"🔴 {symbol}: RSI = {rsi_value:.2f} — Overbought"

    return None


if __name__ == "__main__":
    import asyncio
    from data_fetcher import fetch_all_symbols

    async def test():
        data = await fetch_all_symbols()
        for symbol, df in data.items():
            df_with_indicators = calculate_indicators(df)
            print(f"\n{symbol}:")
            print(df_with_indicators[["timestamp", "close", "rsi", "sma"]].tail(5))

            signal = check_signal(df_with_indicators, symbol)
            if signal:
                print(signal)
            else:
                print(f"{symbol}: no signal (RSI in normal range)")

    asyncio.run(test())
