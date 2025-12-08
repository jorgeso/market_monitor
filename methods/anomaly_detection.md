# Anomaly Detection

Credit: [How to Detect Anomalies in Time Series Data in Python](https://www.statology.org/how-to-detect-anomalies-in-time-series-data-in-python/)

I followed the article above to create a method for detecting anomalies in the Apple stock. Since I'm trying to create an up-to-date notification system. I tested with data from the last 14 days, 1-hour intervals, and calculated the rolling mean using 5-hour windows. I tested different z-score thresholds and determined a threshold of 3 was the most reasonable.

Here's the data I used to test and visualize the data:

```
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

ticker = "AAPL"

stock_data = yf.Ticker(ticker).history(interval="1h", period="14d", prepost=True).dropna()
stock_data["percentage_change"] = stock_data["Close"].pct_change() * 100
stock_data.reset_index(drop=True, inplace=True)

rolling_window = 5
threshold = 3

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

    print((np.abs(last_time_step[f'{column}_z_score_rolling']) > threshold).tolist()[0])

    print(last_time_step[column].tolist()[0])

    rolling_anomalies = stock_data[np.abs(stock_data[f'{column}_z_score_rolling']) > threshold]

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data.index, stock_data[column], label=colum_label_map[column], alpha=0.6)
    plt.scatter(rolling_anomalies.index, rolling_anomalies[column], color='red', label='Rolling Z-Score Anomalies')
    plt.plot(rolling_mean, color='green', label='Rolling Mean')
    plt.fill_between(stock_data.index,
                    rolling_mean - threshold * rolling_std,
                    rolling_mean + threshold * rolling_std,
                    color='orange', alpha=0.2, label='Threshold')
    plt.title('Rolling Z-Score Anomaly Detection')
    plt.xlabel('Time Step')
    plt.ylabel(colum_label_map[column])
    plt.legend()
    plt.grid()
    plt.show()
```

Notice that I droped the date-time index and substituted them with simple integer indices `stock_data.reset_index(drop=True, inplace=True)`. This is simply so the plots don't have big gaps in the times that the market was closed and didn't produce any data.

The plots from my testing are here:

![Rolling Z-Score Anomaly Detection - price](/methods/img/rolling_z-score_anomaly_detection_price.png)
![Rolling Z-Score Anomaly Detection - % change](/methods/img/rolling_z-score_anomaly_detection_change.png)
