import yfinance as yf

def is_market_open() -> bool:

    sp500 = "^GSPC"
    stock_data = yf.Ticker(sp500).history(interval="1m", period="1m")
    return len(stock_data) > 0