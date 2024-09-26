def fetch_market_data(symbol, start_date, end_date, interval='1d'):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return data

# Example usage
data = fetch_market_data('EURUSD=X', '2020-01-01', '2023-01-01')
print(data.head())