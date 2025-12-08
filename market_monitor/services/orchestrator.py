from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
from time import sleep
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
                    f"zone. Average % change over the last 4 hours is {pct_change:.4f}"
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


def start_monitoring_market():
    send_notification(message=f"starting to monitor market", to_admin=True)
    end_datetime = datetime.now().astimezone(ZoneInfo("America/New_York")).replace(hour=20, minute=0, second=0, microsecond=0)
    in_monitor_time = True
    while in_monitor_time:
        try:
            now = datetime.now().astimezone(ZoneInfo("America/New_York"))
            in_monitor_time = now <= end_datetime
            perform_market_check()
            sleep(300)
        except Exception as e:
            in_monitor_time = False
            send_notification(message=f"application problem {str(e)}", to_admin=True)
    send_notification(message=f"market monitoring ended", to_admin=True)
        
            

            
