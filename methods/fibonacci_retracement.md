# Fibonacci Retracement

Credit: 
- [How to Use Fibonacci Retracement in Tradingview](https://www.youtube.com/watch?v=S4B5g96A2lg)
- [Fibonacci Retracement Explained and Modelled in Python](https://medium.com/jpa-quant-articles/fibonacci-retracement-in-python-17165e51f92c)

According the video above, it is beneficial to know when the price of a stock is between two values derived from calcutions made using ratios related to the Fibonacci sequence. For example, using Apple stock data, the area of interest (or the "golden zone" in the video) would be the red are in the following graph:

![Apple golden zone](/methods/img/fibonacci_retracement.png)

I didn't confirm the validity of the claim in the video, I just decided to learn a little more about Fibonnaci retracement, and then create a notfication that would let me know when any given stock is in the "golden zone."

The code for recreating the plot above is here:

```
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

ticker = "AAPL"

stock_data = yf.Ticker(ticker).history(interval="1h", period="14d", prepost=True).dropna()
stock_data["percentage_change"] = stock_data["Close"].pct_change() * 100
stock_data.reset_index(drop=True, inplace=True)

# Fibonacci constants
max_value = stock_data['Close'].max()
min_value = stock_data['Close'].min()
difference = max_value - min_value

# Set Fibonacci levels
first_level = max_value - difference * 0.236
second_level = max_value - difference * 0.382
third_level = max_value - difference * 0.5
fourth_level = max_value - difference * 0.618

stock_data["is_golden_zone"] = ((stock_data['Close'] > second_level) & (stock_data['Close'] > fourth_level))

print(stock_data.tail(1)["is_golden_zone"])

# Print levels
print('Percentage level\t Price')
print('0.00%\t\t', round(min_value, 3))
print('23.6%\t\t', round(first_level, 3))
print('38.2%\t\t', round(second_level, 3))
print('50%\t\t', round(third_level, 3))
print('61.8%\t\t', round(fourth_level, 3))
print('100.00%\t\t', round(max_value, 3))

# Plot Fibonacci graph
plot_title = 'Fibonacci Retracement for ' + ticker
fig = plt.figure(figsize=(14, 7))




ax = fig.add_subplot()
# fig, ax = plt.subplots()
ax.set_title(plot_title, fontsize=30)

ax.plot(stock_data.index, stock_data['Close'])

# plt.axhline(max_value, linestyle='--', alpha=0.5, color='purple')
# ax.fill_between(stock_data.index, max_value, first_level, color='purple', alpha=0.2)

# Fill sections
ax.axhline(first_level, linestyle='--', alpha=0.5, color='blue', label="0.236")
# ax.fill_between(stock_data.index, first_level, second_level, color='blue', alpha=0.2)

ax.axhline(second_level, linestyle='--', alpha=0.5, color='green', label="0.382")
# ax.fill_between(stock_data.index, second_level, third_level, color='green', alpha=0.2)

ax.axhline(third_level, linestyle='--', alpha=0.5, color='red', label="0.5")
# ax.fill_between(stock_data.index, third_level, fourth_level, color='red', alpha=0.2)

ax.axhline(fourth_level, linestyle='--', alpha=0.5, color='orange', label="0.618")
# ax.fill_between(stock_data.index, fourth_level, min_value, color='orange', alpha=0.2)

ax.fill_between(stock_data.index, second_level, fourth_level, color='red', alpha=0.2)

# ax.axhline(min_value, linestyle='--', alpha=0.5, color='yellow')

ax.legend()
ax.set_xlabel('Time Step', fontsize=20)
ax.set_ylabel('Close Price (USD)', fontsize=20)
```