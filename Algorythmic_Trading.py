import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tsla = pdr.get_data_yahoo('TSLA', start=datetime.datetime(2005,1,1), end=datetime.datetime(2020,1,1))
#Download data from yahoo finance, Quandl also works
print(tsla.tail())

tsla['Close'].plot(grid=True)
plt.show()
#graph data to show that data is correct

#Assign 'Adj Close' to 'Daily Close'
daily_close= tsla[['Adj Close']]

#daily returns
daily_pct_change = daily_close.pct_change()

#clean data; replace NA with 0
daily_pct_change.fillna(0, inplace=True)

#Cumulative daily return
cum_daily_return = (1 + daily_pct_change).cumprod()
#plot
cum_daily_return.plot(figsize=(12,8))
plt.show()

#verify
print(daily_pct_change)

#log in order to scale the data
daily_log_returns = np.log(daily_close.pct_change()+1)

#verify
print(daily_log_returns)

#resample as monthly
monthly= tsla.resample('BM').apply(lambda x: x[-1])
#pct pct_change
monthly.pct_change()
#resample to quarters using the mean()
quarter= tsla.resample('4M').mean()
#quarterly pct pct_chang
quarter.pct_change()
