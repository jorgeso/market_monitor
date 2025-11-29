# Anomaly Detection

Credit: [How to Detect Anomalies in Time Series Data in Python](https://www.statology.org/how-to-detect-anomalies-in-time-series-data-in-python/)

I followed the article above to create a method for detecting anomalies in the S&P 500. Since I'm trying to create an up-to-date notification system. I tested with data over the last 7 days, 1-minute intervals, an 60-minute rolling time steps. I tested different z-score thresholds and determined a threshold of 4 was the most reasonable.

Here's the data I used to test and visualize the data:

```
from datetime import datetime
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

ticker = "^GSPC"

stock_data = yf.Ticker(ticker).history(interval="1m", period="7d").dropna()
stock_data["percentage_change"] = stock_data["Close"].pct_change() * 100
stock_data.reset_index(drop=True, inplace=True)
len(stock_data)

rolling_window = 60
threshold = 4

rolling_mean = stock_data["percentage_change"].rolling(window=rolling_window, closed="left").mean()
rolling_std = stock_data["percentage_change"].rolling(window=rolling_window, closed="left").std()

stock_data['z_score_rolling'] = (stock_data["percentage_change"] - rolling_mean) / rolling_std

rolling_anomalies = stock_data[np.abs(stock_data['z_score_rolling']) > threshold]

plt.figure(figsize=(14, 7))
plt.plot(stock_data.index, stock_data["percentage_change"], label='Stock % Change', alpha=0.6)
plt.scatter(rolling_anomalies.index, rolling_anomalies["percentage_change"], color='red', label='Rolling Z-Score Anomalies')
plt.plot(rolling_mean, color='green', label='30-minute Rolling Mean')
plt.fill_between(stock_data.index,
                 rolling_mean - threshold * rolling_std,
                 rolling_mean + threshold * rolling_std,
                 color='orange', alpha=0.2, label='Threshold')
plt.title('Rolling Z-Score Anomaly Detection')
plt.xlabel('Time Step')
plt.ylabel('Stock % Change')
plt.legend()
plt.grid()
plt.show()
```

Notice that droped the date-time index for simple integer indices `stock_data.reset_index(drop=True, inplace=True)`. This is simply so the plots don't have big gaps in the times that the market was closed and didn't produce any data.

The plot from my testing is here:

![Rolling Z-Score Anomaly Detection](/methods/img/rolling_z-score_anomaly_detection.png)