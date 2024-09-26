import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Alpaca API keys
API_KEY = 'your-api-key'
SECRET_KEY = 'your-secret-key'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use this URL for paper trading, change to live URL for live trading

# Connect to Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Fetch account information
account = api.get_account()
print(f"Cash Balance: ${account.cash}")
