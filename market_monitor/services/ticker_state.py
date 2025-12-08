from os.path import exists
from json import load, dump
from os import environ
from typing import Union, Dict
from market_monitor.services.utilities import get_tickers_to_watch

_TICKER_STATE = None

def load_ticker_state():
    global _TICKER_STATE

    root_path = environ["MARKET_MONITOR_PATH"]
    ticker_states_path = f"{root_path}/ticker_states.json"

    if exists(ticker_states_path):
        with open(ticker_states_path, "r") as ticker_states_file:
            _TICKER_STATE = load(ticker_states_file)
    else:
        _TICKER_STATE = {}

    tickers = get_tickers_to_watch()
    for ticker in tickers:
        if ticker not in _TICKER_STATE:
            _TICKER_STATE[ticker] = {}


def dump_ticker_state():
    root_path = environ["MARKET_MONITOR_PATH"]
    ticker_states_path = f"{root_path}/ticker_states.json"
    with open(ticker_states_path, "w") as ticker_states_file:
        dump(_TICKER_STATE, ticker_states_file)

def update_ticker_state(ticker: str, key: str, value: Union[str, int, bool, float]):
    _TICKER_STATE[ticker][key] = value
    dump_ticker_state()

def get_ticker_state(ticker: str) -> Dict[str, Union[str, int, bool, float]]:
    return _TICKER_STATE[ticker]