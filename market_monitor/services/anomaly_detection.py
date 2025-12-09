import yfinance as yf
import numpy as np

def check_for_anomalies(ticker: str, interval: str="5m", period: str="10d", rolling_window=10, threshold = 3):

    anomalies = []
    stock_data = yf.Ticker(ticker).history(interval=interval, period=period, prepost=True).dropna()
    if len(stock_data) == 0:
        return anomalies

    stock_data["percentage_change"] = stock_data["Close"].pct_change() * 100

    columns = ["Close", "percentage_change"]

    colum_label_map = {
        "Close": "Stock Price",
        "percentage_change": "Stock % Change"
    }

    for column in columns:

        rolling_mean = stock_data[column].rolling(window=rolling_window, closed="left").mean()
        rolling_std = stock_data[column].rolling(window=rolling_window, closed="left").std()

        stock_data[f'{column}_z_score_rolling'] = (stock_data[column] - rolling_mean) / rolling_std

        last_time_step = stock_data.tail(1)

        is_anomaly = (np.abs(last_time_step[f'{column}_z_score_rolling']) > threshold).tolist()[0]

        if is_anomaly:
            anomaly_value = last_time_step[column].tolist()[0]
            anomaly = {
                "property": colum_label_map[column],
                "value": anomaly_value
            }
            anomalies.append(anomaly)

        return anomalies