# Initial capital
initial_capital = 10000
data['Daily Returns'] = data['Close'].pct_change()  # Daily returns of the asset

# Apply strategy: multiply daily returns by the position
data['Strategy Returns'] = data['Daily Returns'] * data['Position']

# Calculate cumulative returns
data['Cumulative Strategy Returns'] = (1 + data['Strategy Returns']).cumprod()
data['Cumulative Buy and Hold Returns'] = (1 + data['Daily Returns']).cumprod()

# Plot the results
plt.figure(figsize=(12, 8))
plt.plot(data['Cumulative Strategy Returns'], label='Strategy Returns', color='green')
plt.plot(data['Cumulative Buy and Hold Returns'], label='Buy and Hold Returns', color='blue')
plt.title('Momentum Trading Strategy vs Buy and Hold')
plt.legend()
plt.show()

# Final portfolio values
final_strategy_value = initial_capital * data['Cumulative Strategy Returns'].iloc[-1]
final_buy_hold_value = initial_capital * data['Cumulative Buy and Hold Returns'].iloc[-1]

print(f"Final Portfolio Value (Strategy): ${final_strategy_value:.2f}")
print(f"Final Portfolio Value (Buy and Hold): ${final_buy_hold_value:.2f}")
