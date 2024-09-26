def execute_trade(signal, symbol='AAPL', qty=10):
    if signal == 1:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print("Buy order executed")
    elif signal == -1:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print("Sell order executed")

# Example of using the strategy to make trades
current_rsi = 55  # Replace this with your RSI calculation
if current_rsi > 50:  # Momentum is positive
    execute_trade(1)
elif current_rsi < 50:  # Momentum is negative
    execute_trade(-1)