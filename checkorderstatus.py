# Get a list of orders
orders = api.list_orders(status='open')  # You can specify 'all', 'open', 'closed'

for order in orders:
    print(f"Order for {order.symbol}: Status - {order.status}, Quantity - {order.qty}")
