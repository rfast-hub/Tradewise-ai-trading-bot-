# Create a new 'Signal' column where 1 = Buy, -1 = Sell
data['Signal'] = 0  # Default is no signal

# Buy signal: RSI > 50 and EMA50 > EMA200 (momentum up)
data['Signal'] = np.where((data['RSI'] > 50) & (data['EMA50'] > data['EMA200']), 1, data['Signal'])

# Sell signal: RSI < 50 and EMA50 < EMA200 (momentum down)
data['Signal'] = np.where((data['RSI'] < 50) & (data['EMA50'] < data['EMA200']), -1, data['Signal'])

# Add position based on the signal (shift signal to avoid lookahead bias)
data['Position'] = data['Signal'].shift()

# Show data with signals
print(data[['Close', 'RSI', 'EMA50', 'EMA200', 'Signal']].tail())
