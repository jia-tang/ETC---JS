prod_limits = {}

live_buy_prices = {}
live_sell_prices = {}

live_buy_avg = {}
live_sell_avg = {}

prod_types = ['BOND', 'VALE', 'VALBZ', 'GS', 'MS', 'WFC', 'XLF']
prod_limits["BOND"] = 100
prod_limits['VALE'] = 10
prod_limits['VALBZ'] = 10
prod_limits['GS'] = 100
prod_limits['MS'] = 100
prod_limits['WFC'] = 100
prod_limits['XLF'] = 100

while True:
    message = read_from_exchange(exchange)
    if message["type"] == "book":
        prod = message["symbol"]
        live_buy_prices[prod] = message['buy'][0][0]
        live_sell_prices[prod] = message['sell'][0][0]


    # if message["symbol"] == "BOND":
    #
    # elif message["symbol"] == "VALE":
    # elif message["symbol"] == "VALEBZ":
    # elif message["symbol"] == "GS":
    # elif message["symbol"] == "MS":
    # elif message["symbol"] == "WFC":
    # elif message["symbol"] == "XLF":




#     print(message)
# if message["type"] == "fill" or message["type"] == "hello":
#     print(message)
