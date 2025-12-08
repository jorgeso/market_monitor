from os import environ
from os.path import exists
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional
import yfinance as yf

def is_market_open() -> bool:

    sp500 = "^GSPC"
    stock_data = yf.Ticker(sp500).history(interval="1m", period="1d")
    if len(stock_data) == 0:
        return False
    last_data_datetime = stock_data.index[-1]
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)
    five_minutes_ago = five_minutes_ago.replace(tzinfo=last_data_datetime.tzinfo)

    return last_data_datetime > five_minutes_ago

def has_data(ticker) -> bool:
    stock_data = yf.Ticker(ticker=ticker).history(interval="1m", period="1d", prepost=True)
    if len(stock_data) == 0:
        return False
    last_data_datetime = stock_data.index[-1]
    now = datetime.now()
    one_hour_ago = now - timedelta(minutes=60)
    one_hour_ago = one_hour_ago.replace(tzinfo=last_data_datetime.tzinfo)

    return last_data_datetime > one_hour_ago

def get_last_ticker_data(ticker: str) -> Optional[Dict[str, Union[int, float]]]:

    stock_data = yf.Ticker(ticker).history(interval="1d", period="2d")
    if len(stock_data) == 0:
        return None
    stock_data["%Change"] = stock_data["Close"].pct_change()
    stock_data.drop(columns=["Volume", "Dividends", "Stock Splits"], inplace=True)
    last_item = stock_data.tail(1)
    last_item_dict = last_item.to_dict("records")[0]
    return last_item_dict

def get_ticker_mean_pct_change(ticker: str) -> float:
    stock_data = yf.Ticker(ticker).history(interval="1h", period="1d", prepost=True).dropna()
    stock_data["percentage_change"] = stock_data["Close"].pct_change()
    return stock_data["percentage_change"].dropna().mean()


def create_system_status_file():
    root_path = environ["MARKET_MONITOR_PATH"]
    system_market_status_path = f"{root_path}/system_market_status"

    if not exists(system_market_status_path):
        toggle_system_market_status(new_status=False)


def is_system_market_status_open() -> bool:
    root_path = environ["MARKET_MONITOR_PATH"]

    with open(f"{root_path}/system_market_status", "r") as market_open_file:
        system_market_status = market_open_file.read()
    is_system_market_status_open = bool(int(system_market_status))
    return is_system_market_status_open

def toggle_system_market_status(new_status: bool):
    new_status_str = str(int(new_status))

    root_path = environ["MARKET_MONITOR_PATH"]

    with open(f"{root_path}/system_market_status", "w") as market_open_file:
        market_open_file.write(new_status_str)

def get_tickers_to_watch() -> List[str]:

    root_path = environ["MARKET_MONITOR_PATH"]

    with open(f"{root_path}/watch_tickers", "r") as watch_tickers_file:
        watch_tickers_str = watch_tickers_file.read()
    
    watch_tickers_list = [row.strip() for row in watch_tickers_str.split("\n") if row.strip() != ""]

    return watch_tickers_list