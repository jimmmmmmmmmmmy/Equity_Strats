import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Download data
data_spy = yf.download('SPY')
data_spxl = yf.download('SPXL')

# Calculate price change for SPY
data_spy['PriceChange'] = data_spy['Close'] - data_spy['Open']
red_days = data_spy[data_spy['PriceChange'] < 0].index

# Initialize variables
cash_spy_spxl = cash_spy = cash_hold = 100000
equity_curve_spy_spxl = []
equity_curve_spy_only = []
transaction_days_spy_spxl = []
transaction_days_spy_only = []

# Calculate equity curve for SPY/SPXL strategy
for i in range(len(red_days) - 1):
    if red_days[i] in data_spy.index:
        buy_price_spy = data_spy.loc[red_days[i]]['Close']
        buy_price_spy_spxl = data_spxl.loc[red_days[i]]['Close'] if red_days[i] in data_spxl.index else buy_price_spy

        if red_days[i] + pd.DateOffset(1) in data_spy.index:
            sell_price_spy = data_spy.loc[red_days[i] + pd.DateOffset(1)]['Close']
            sell_price_spy_spxl = data_spxl.loc[red_days[i] + pd.DateOffset(1)]['Close'] if red_days[i] + pd.DateOffset(1) in data_spxl.index else sell_price_spy

            shares_spy_spxl = cash_spy_spxl / buy_price_spy_spxl
            cash_spy_spxl = shares_spy_spxl * sell_price_spy_spxl
            equity_curve_spy_spxl.append((cash_spy_spxl / cash_hold - 1) * 100)  # Convert to percentage
            transaction_days_spy_spxl.append(red_days[i])

            # Calculate equity curve for SPY only strategy
            shares_spy_only = cash_spy / buy_price_spy
            cash_spy = shares_spy_only * sell_price_spy
            equity_curve_spy_only.append((cash_spy / cash_hold - 1) * 100)  # Convert to percentage
            transaction_days_spy_only.append(red_days[i])

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)

plt.plot(transaction_days_spy_spxl, equity_curve_spy_spxl, label='jimjam gatdamn SPY/SPXL', color='blue')
plt.title('Equity Curve for SPY/SPXL')
plt.ylabel('Equity')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())  # Add % to y-axis labels
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(transaction_days_spy_only, equity_curve_spy_only, label='jimjam SPY only', color='green')
plt.title('Equity Curve for SPY only')
plt.ylabel('Equity')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())  # Add % to y-axis labels
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(data_spy.index, (cash_hold * data_spy['Close'] / data_spy.loc[data_spy.index[0]]['Close'] / cash_hold - 1) * 100, label='Buy and hold SPY', color='red')  # Convert to percentage
plt.title('Equity Curve for Buy and Hold SPY')
plt.xlabel('Transaction Days')
plt.ylabel('Equity')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())  # Add % to y-axis labels
plt.legend()

plt.tight_layout()
plt.show()