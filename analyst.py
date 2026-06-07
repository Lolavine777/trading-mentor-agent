import pandas as pd
import pandas_ta as ta
from vnstock.api.quote import Quote
from datetime import datetime, timedelta


def get_history(symbol: str, days: int = 120) -> pd.DataFrame:
    end = datetime.today().strftime("%Y-%m-%d")
    start = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    q = Quote(symbol=symbol, source="VCI")
    df = q.history(start=start, end=end)
    df = df.rename(columns={"time": "date"})
    df = df.sort_values("date").reset_index(drop=True)
    return df


def calculate_indicators(df: pd.DataFrame) -> dict:
    close = df["close"]
    volume = df["volume"]

    # RSI
    rsi_series = ta.rsi(close, length=14)
    rsi = round(float(rsi_series.iloc[-1]), 2)

    # MACD
    macd_df = ta.macd(close, fast=12, slow=26, signal=9)
    macd = round(float(macd_df["MACD_12_26_9"].iloc[-1]), 2)
    signal = round(float(macd_df["MACDs_12_26_9"].iloc[-1]), 2)

    # EMA
    ema20_series = ta.ema(close, length=20)
    ema50_series = ta.ema(close, length=50)
    ema20 = round(float(ema20_series.iloc[-1]), 2) if ema20_series is not None else None
    ema50 = round(float(ema50_series.iloc[-1]), 2) if ema50_series is not None else None

    # Volume so với trung bình 20 phiên
    avg_volume = round(float(volume.rolling(20).mean().iloc[-1]), 0)
    last_volume = int(volume.iloc[-1])
    volume_ratio = round(last_volume / avg_volume, 2)

    # Giá
    last_close = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    change_pct = round((last_close - prev_close) / prev_close * 100, 2)

    # Interpretation
    if rsi > 70:
        rsi_note = "overbought, cẩn thận chốt lời"
    elif rsi < 30:
        rsi_note = "oversold, nhưng kiểm tra trend trước khi mua"
    else:
        rsi_note = "trung tính"

    macd_note = "bullish" if macd > signal else "bearish"

    if volume_ratio > 1.5:
        vol_note = f"cao bất thường ({volume_ratio}x TB)"
    elif volume_ratio < 0.7:
        vol_note = f"thấp ({volume_ratio}x TB)"
    else:
        vol_note = f"bình thường ({volume_ratio}x TB)"

    if ema20 is not None and ema50 is not None:
        trend = "uptrend" if ema20 > ema50 else "downtrend"
    elif ema20 is not None:
        trend = "uptrend" if close.iloc[-1] > ema20 else "downtrend"
    else:
        trend = "unknown"

    return {
        "symbol": df.get("symbol", [""])[0] if "symbol" in df.columns else "",
        "close": last_close,
        "change_pct": change_pct,
        "volume": last_volume,
        "volume_note": vol_note,
        "rsi": rsi,
        "rsi_note": rsi_note,
        "macd": macd,
        "macd_signal": signal,
        "macd_note": macd_note,
        "ema20": ema20,
        "ema50": ema50,
        "trend": trend,
        "interpretation": (
            f"RSI {rsi} ({rsi_note}), MACD {macd_note}, "
            f"volume {vol_note}, trend {trend}"
        )
    }


def analyze_stock(symbol: str) -> dict:
    df = get_history(symbol, days=120)
    return calculate_indicators(df)


def analyze_portfolio(symbols: list) -> list:
    results = []
    for symbol in symbols:
        try:
            result = analyze_stock(symbol)
            result["symbol"] = symbol
            results.append(result)
        except Exception as e:
            results.append({"symbol": symbol, "error": str(e)})
    return results