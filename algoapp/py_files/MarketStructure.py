import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MarketStruct:
    lowpoint  = 99999999999
    def AnalysMarketStruct(marketdetails):
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(marketdetails, columns=columns)

        # Convert Date column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])
        # Calculate moving averages (50-day and 200-day)
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()

        # Initialize a column for trading signals
        df['Signal'] = 0

        # Generate buy signals when MA50 crosses above MA200
        df.loc[df['MA50'] > df['MA200'], 'Signal'] = 1

        # Generate sell signals when MA50 crosses below MA200
        df.loc[df['MA50'] < df['MA200'], 'Signal'] = -1

        # Calculate daily returns based on signal
        df['Returns'] = df['Signal'].shift(1) * df['Close'].pct_change()

        # Calculate cumulative returns
        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()

        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Cumulative_Returns'])
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.title('Moving Average Crossover Strategy')
        plt.grid(True)
        plt.show()



       
