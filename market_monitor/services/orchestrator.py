from typing import List
from market_monitor.services.utilities import (
    is_market_open,
    get_tickers_to_watch,
    get_last_ticker_data,
    is_system_market_status_open,
    toggle_system_market_status,
    has_data,
    create_system_status_file
)
from market_monitor.services.notifications import send_notification
from market_monitor.services.anomaly_detection import check_for_anomalies
from market_monitor.services.fibonacci_retracement import is_in_golden_zone
from market_monitor.services.ticker_state import load_ticker_state, get_ticker_state, update_ticker_state

def _check_indicators(tickers_to_watch: List[str], market_closed: bool):
    for ticker in tickers_to_watch:
        ticker_state = get_ticker_state(ticker=ticker)
        fibonacci_golden_zone_key = "is_in_fibonacci_golden_zone"
        already_in_golden_zone = fibonacci_golden_zone_key in ticker_state and ticker_state[fibonacci_golden_zone_key]
        in_golden_zone, pct_change = is_in_golden_zone(ticker=ticker)
        if market_closed:
            closing_data = get_last_ticker_data(ticker=ticker)
            if closing_data is not None:
                message = ticker + " closing data"
                for key, value in closing_data.items():
                    message += f" {key}={value:.3f},"
                message = message[:-1]
                send_notification(
                    message=message
                )
        if has_data(ticker=ticker):
            anomalies = check_for_anomalies(ticker=ticker)
            for anomaly in anomalies:
                send_notification(
                    message=f"Anomaly detected for {ticker} {anomaly['property']} = {anomaly['value']}"
                )
            if in_golden_zone and not already_in_golden_zone:
                fibonacci_message = (
                    f"Fibonacci retracement analysis shows that {ticker} has entered its golden "
                    f"zone. % change over the last day is {pct_change:.4f}"
                )
                send_notification(
                    message=fibonacci_message
                )
                update_ticker_state(ticker=ticker, key=fibonacci_golden_zone_key, value=True)
            elif already_in_golden_zone and not in_golden_zone:
                send_notification(
                    message=f"Fibonacci retracement analysis shows that {ticker} has exited its golden zone."
                )
                update_ticker_state(ticker=ticker, key=fibonacci_golden_zone_key, value=False)

def perform_market_check():

    create_system_status_file()
    load_ticker_state()
    tickers_to_watch = get_tickers_to_watch()
    market_closed = False

    if is_market_open():
        if not is_system_market_status_open():
            toggle_system_market_status(True)
            send_notification(
                message="Market is open."
            )
    else:
        if is_system_market_status_open():
            market_closed = True
            toggle_system_market_status(False)
            send_notification(
                message="Market is closed."
            )

    _check_indicators(
        tickers_to_watch=tickers_to_watch,
        market_closed=market_closed
    )
        
            

            
