import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# Download historical data for EUR/USD
data = yf.download('EURUSD=X', start='2020-01-01', end='2023-01-01', interval='1d')

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate short-term and long-term EMAs
data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

# Calculate RSI
data['RSI'] = calculate_rsi(data)

# Drop rows with NaN values
data.dropna(inplace=True)

# Create a new 'Signal' column where 1 = Buy, -1 = Sell
data['Signal'] = 0  # Default is no signal
data['Signal'] = np.where((data['RSI'] > 50) & (data['EMA50'] > data['EMA200']), 1, data['Signal'])
data['Signal'] = np.where((data['RSI'] < 50) & (data['EMA50'] < data['EMA200']), -1, data['Signal'])

# Add position based on the signal (shift signal to avoid lookahead bias)
data['Position'] = data['Signal'].shift()

# Initial capital
initial_capital = 10000
data['Daily Returns'] = data['Close'].pct_change()  # Daily returns of the asset
data['Strategy Returns'] = data['Daily Returns'] * data['Position']

# Calculate cumulative returns
data['Cumulative Strategy Returns'] = (1 + data['Strategy Returns']).cumprod()
data['Cumulative Buy']

def main():
    symbol = 'EURUSD=X'
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    interval = '1d'

    # Fetch market data
    data = fetch_market_data(symbol, start_date, end_date, interval)

    # Generate buy/sell signals
    data = generate_signals(data)

    # Backtest the strategy
    backtest_strategy(data)

    # Execute trades based on signals
    for index, row in data.iterrows():
        execute_trade(row['Signal'], symbol=symbol)

    # Monitor order status
    check_order_status()

if __name__ == "__main__":
    main()
