prod_types = ['BOND', 'VALUE', 'VALBZ', 'GS', 'MS', 'WFC', 'XLF']
live_buy_prices = {}
live_sell_prices = {}

live_buy_avg = {}
live_sell_avg = {}

for prod in prod_types:
    live_buy_prices[prod] = 0
    live_sell_prices[prod] = 0

    live_buy_avg[prod] = 0
    live_sell_avg[prod] = 0

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
