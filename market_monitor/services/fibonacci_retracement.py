import yfinance as yf
from typing import Tuple
from market_monitor.services.utilities import get_ticker_mean_pct_change

def is_in_golden_zone(ticker: str, interval: str="5m", period: str="10d") -> Tuple[bool, float]:
    stock_data = yf.Ticker(ticker).history(interval=interval, period=period).dropna()
    # Fibonacci constants
    max_value = stock_data['Close'].max()
    min_value = stock_data['Close'].min()
    difference = max_value - min_value

    # Set Fibonacci levels
    second_level = max_value - difference * 0.382
    fourth_level = max_value - difference * 0.618

    last_item = stock_data.tail(1)
    close = last_item["Close"].to_list()[0]
    ticker_in_golden_zone = bool((close > second_level) and (close > fourth_level))
    pct_change = get_ticker_mean_pct_change(ticker=ticker)
    return (ticker_in_golden_zone, pct_change)