#!/usr/bin/python
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json

from timeit import default_timer as timer
from datetime import timedelta
# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name = "teamync"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 0
prod_exchange_hostname = "production"

port = 25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile("rw", 1)


def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read_from_exchange(exchange):
    return json.loads(exchange.readline())

# ~~~~~============== Helper ==============~~~~~

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


# ~~~~~============== MAIN LOOP ==============~~~~~


def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    
    buy_bond = {"type": "add", "order_id": 1, "symbol": "BOND", "dir": "BUY", "price": 999, "size": 1}
    sell_bond = {"type": "add", "order_id": 2, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 1}
    cancel_buy = {"type": "cancel", "order_id": 1}
    write_to_exchange(exchange, buy_bond)
    write_to_exchange(exchange, sell_bond)
    

    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    
    start = timer()
    while True:
       # if sell and price <= 1k, BUY
        message = read_from_exchange(exchange)
        # if message["type"] == "book" and message["symbol"] == "VALE":
        #     print(message)
        # if message["type"] == "fill" or message["type"] == "VALEBZ": 
        #     print(message)

        if message["type"] == "book":
            prod = message["symbol"]
            live_buy_prices[prod] = message['buy'][0][0]
            live_sell_prices[prod] = message['sell'][0][0]
            VALE_sell = live_sell_prices["VALE"]
            VALE_buy = live_buy_prices["VALE"]
            VALBZ_sell = live_sell_prices["VALBZ"]
            VALBZ_buy = live_buy_prices["VALBZ"]

            if VALE_buy < VALBZ_sell:
                buy_VALE = {"type": "add", "order_id": 3, "symbol": "VALE", "dir": "BUY", "price": VALE_buy, "size": 10}
                sell_VALBZ = {"type": "add", "order_id": 4, "symbol": "VALBZ", "dir": "SELL", "price": VALBZ_sell, "size": 10}
                write_to_exchange(exchange, buy_VALE)
                write_to_exchange(exchange, sell_VALBZ)

            if VALE_sell < VALBZ_buy:
                buy_VALE = {"type": "add", "order_id": 3, "symbol": "VALE", "dir": "BUY", "price": VALE_sell, "size": 10}
                sell_VALBZ = {"type": "add", "order_id": 4, "symbol": "VALBZ", "dir": "SELL", "price": VALBZ_buy, "size": 10}
                write_to_exchange(exchange, buy_VALE)
                write_to_exchange(exchange, sell_VALBZ)

        if message["type"] == "fill": 
            print(message)






    #  now = timer()
    #  if int(timedelta(seconds = now-start)) % 30 == 0:
    #    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    #   # print(type(message))
    #   #  print(message)
        if message["type"] == "close":
            print("The round has ended")
            break


if __name__ == "__main__":
    main()
