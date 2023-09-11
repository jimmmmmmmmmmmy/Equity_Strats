import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download('SPY')
data['PriceChange'] = data['Close'] - data['Open']
red_days = data[data['PriceChange'] < 0].index

cash = 100000
equity_curve = []
transaction_days = []

for i in range(len(red_days) - 1):
    if red_days[i] in data.index:
        buy_price = data.loc[red_days[i]]['Close']
        if red_days[i] + pd.DateOffset(1) in data.index:
            sell_price = data.loc[red_days[i] + pd.DateOffset(1)]['Close']
            shares = cash / buy_price
            cash = shares * sell_price
            equity_curve.append(cash)
            transaction_days.append(red_days[i])

equity_curve_percent = pd.Series(equity_curve, index=transaction_days) / 1000  # Convert equity curve to percent of starting balance

equity_curve_percent.plot(title='Equity Curve')
plt.ylabel('Equity (%)')
plt.show()