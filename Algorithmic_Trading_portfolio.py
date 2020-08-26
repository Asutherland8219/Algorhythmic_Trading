from typing import Union
from GoogleNews import GoogleNews
import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, Series
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import yfinance as yf


yf.pdr_override




input_string = input("Enter Tickers you wish to Analyze, seperated by comma: ")
input_vol = input("Please enter the minimum period(s) [Starting point = start date + min period] of volatitility you would like to analyze: ")
input_start = input("Please enter your desired start date (YYYY-MM-DD): ")
input_end = input("Please enter your desired end date (YYYY-MM-DD): ")

startdate = pd.to_datetime(input_start, format = "%Y-%m-%d")
enddate = pd.to_datetime(input_end, format = "%Y-%m-%d")

ticker_list = input_string.split(",")
print("Tickers Selected: "+input_string)

tickers= ticker_list

def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker,start=startdate,end=enddate))
    datas = map(data, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker','Date']))
all_data: Union[DataFrame, Series] = get(tickers, startdate, enddate).dropna()

all_data
print(all_data)

daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date','Ticker','Adj Close')

#calculate daily pct change
daily_pct_change = daily_close_px.pct_change()

daily_pct_change.dropna()

daily_log_returns = np.log(daily_close_px.pct_change()+1)


#cumulative daily pct change
cum_daily_return = (1 + daily_pct_change).cumprod()
#plot
fig1 = cum_daily_return.plot(figsize=(12,8))
plt.xlim()
plt.show()


#plot distributions
fig2= daily_pct_change.hist(bins=50,sharex=True, figsize=(12,8))
plt.show()

#create a scatter matrix with daily_pct_change data
fig3= pd.plotting.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1, figsize=(12,12))
plt.show()

#create moving averagees short = 1 quarter, long = 3 quarter
short = daily_close_px.rolling(window=40).mean()
long = daily_close_px.rolling(window=252).mean()


plt.show()


fig4= plt.plot(short)
plt.xlabel('Year')
plt.xlim()
plt.ylabel('Price')
plt.legend(short)
plt.title("Short Rolling")
plt.show()

fig5= plt.plot(long)
plt.xlabel('Year')
plt.xlim()
plt.ylabel('Price')
plt.legend(long)
plt.title("Long Rolling")
plt.show()



#create volatility plot
min_periods= int(input_vol)
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
scaler = StandardScaler()
scaler = scaler.fit(vol)
fig6= vol.plot(figsize=(16,8), title='Percent change based on '+ input_vol + ' days.')
plt.legend()
plt.title("Volatility chart")
plt.show()

#Prompt the user asking if they want to search a certain date and range

def askUser():
    while True:
        try:
            choice = int(input("Do you want to: \n(1)Return to Program start and evaluate more stocks \n(2) Search a date and term to determine what my have driven any volatility \n(3) Proceed to OLS Model with current selection \n(4) Visit my website portfolio"))
        except ValueError:
            print("Please input a number")
            continue
        if 0 < choice < 5:
            break
        else:
            print("That is not between 1 and 4! Try again:")
    print ("You entered: {} ") # Good to use format instead of string formatting with %
mydict = {1:go_to_stackoverflow, 2:import_from_phone, 3:import_from_camcorder, 4:import_from_camcorder}
mydict[choice]()
print(askUser())

s_req = input("Enter the term you would like to search")
st_date = input("Please enter your desired start date (MM-DD-YYY): ")
en_date = input("Please enter your desired end date (MM-DD-YYY): ")

googlenews = GoogleNews()
googlenews.setlang('en')
googlenews.setTimeRange(st_date,en_date)
googlenews.search(s_req)
googlenews.result()




#create a least squares regression model using the variablles
all_adj_close= all_data[['Adj Close']]
all_returns = np.log(all_adj_close / all_adj_close.shift(1))

#isolate the returns you want to value for the OLS
print("As a reminder, you have selected the following: " + input_string)
sample_stocks = input("Please choose 2 of the stocks you have chosen to calculate a OLS regression: ")

reg_choices = sample_stocks.split(",")

print(reg_choices)

# Isolate the first stock returns
item1 = all_returns.iloc[all_returns.index.get_level_values('Ticker') == reg_choices[0]]
item1.index = item1.index.droplevel('Ticker')

# Isolate the 2nd stock  returns
item2 = all_returns.iloc[all_returns.index.get_level_values('Ticker') == reg_choices[1]]
item2.index = item2.index.droplevel('Ticker')

# Build up a new DataFrame with AAPL and MSFT returns
return_data = pd.concat([item1, item2], axis=1)[1:]
return_data.columns = [reg_choices[0], reg_choices[1]]

# Add a constant 
X = sm.add_constant(return_data[reg_choices[0]])

# Construct the model
model = sm.OLS(return_data[reg_choices[1]],X).fit()

# Print the summary
print(model.summary())

# Dep Variable is the response in the Model
# No. Observations is number of prices analyzed
# R - squared : the coefficient of determination. This represents how well the regression line approximates to the real data points. It is how much the model explains variability of the response data around its mean.

plt.plot(item1,item2,'r.')
ax = plt.axis()
x = np.linspace(ax[0], ax[1] + 0.01)

#plot the regression line
plt.plot(x, model.params[0] + model.params[1] * x, 'b',lw=2)
plt.grid(True)
plt.axis('tight')
plt.xlabel(reg_choices[0] + ' returns')
plt.ylabel(reg_choices[1] + ' returns')

plt.show()

win_in= input("Please indicate a trailing trading day window in order to show maximum drawdown during this time period:")
window= int(win_in)
#create max drawdown
rolling_max1 = item1.rolling(window,min_periods=1).max()
daily_drawdown1 = item1/rolling_max1 - 1.0

rolling_max2 = item2.rolling(window,min_periods=1).max()
daily_drawdown2 = item2/rolling_max2 - 1.0

#creat minn daily drawdown
min_daily_drawdown1 = daily_drawdown1.rolling(window,min_periods=1).min()
min_daily_drawdown2 = daily_drawdown2.rolling(window,min_periods=1).min()

#plotting

daily_drawdown1.plot()
min_daily_drawdown1.plot()
plt.show()

daily_drawdown2.plot()
min_daily_drawdown2.plot()
plt.show()

