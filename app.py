from flask import Flask, render_template, request, jsonify
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import numpy as np

app = Flask(__name__)

# Alpaca API keys
API_KEY = 'your-api-key'
SECRET_KEY = 'your-secret-key'
BASE_URL = 'https://paper-api.alpaca.markets'

# Connect to Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

# Function to fetch market data
def fetch_market_data(symbol, start_date, end_date, interval='1d'):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return data

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

# Function to generate buy/sell signals
def generate_signals(data):
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
    data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()
    data['RSI'] = calculate_rsi(data)
    data.dropna(inplace=True)

    data['Signal'] = 0
    data['Signal'] = np.where((data['RSI'] > 50) & (data['EMA50'] > data['EMA200']), 1, data['Signal'])
    data['Signal'] = np.where((data['RSI'] < 50) & (data['EMA50'] < data['EMA200']), -1, data['Signal'])
    data['Position'] = data['Signal'].shift()
    return data

# Function to execute trade
def execute_trade(signal, symbol='AAPL', qty=10):
    if signal == 1:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        return "Buy order executed"
    elif signal == -1:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        return "Sell order executed"
    return "No action taken"

# Function to check order status
def check_order_status():
    orders = api.list_orders(status='open')
    order_list = []
    for order in orders:
        order_list.append({
            'symbol': order.symbol,
            'status': order.status,
            'quantity': order.qty
        })
    return order_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    symbol = request.form['symbol']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    data = fetch_market_data(symbol, start_date, end_date)
    data = generate_signals(data)
    return data.to_json()

@app.route('/execute_trade', methods=['POST'])
def trade():
    signal = int(request.form['signal'])
    symbol = request.form['symbol']
    qty = int(request.form['qty'])
    result = execute_trade(signal, symbol, qty)
    return jsonify({'result': result})

@app.route('/order_status', methods=['GET'])
def order_status():
    orders = check_order_status()
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)