# Market Monitor

This application monitors stocks listed in a file called `watch_tickers` and sends notifications when any of the stocks fall within certain parameters of different indicators. I run this applicaion in a raspberry pie at home.

Here are the indicators included so far:
- [Anomaly detection](methods/anomaly_detection.md)
- [Fibonacci retracement](methods/fibonacci_retracement.md)

Dependencies:
- [Python 3.13](https://www.python.org/downloads/release/python-3130/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Pushover account and API key](https://pushover.net/)

Required environment variables:
```
MARKET_MONITOR_PATH=/path/to/project-root
PUSHOVER_API_KEY
PUSHOVER_GROUP_ID
```