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
test_mode = False

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 1
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


# ~~~~~============== MAIN LOOP ==============~~~~~


def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    
    buy_vale = {"type": "add", "order_id": 1, "symbol": "VALE", "dir": "BUY", "price": 4981, "size": 100}
    buy_bond = {"type": "add", "order_id": 1, "symbol": "BOND", "dir": "BUY", "price": 1000, "size": 100}
    sell_bond = {"type": "add", "order_id": 2, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 10}
    cancel_buy = {"type": "cancel", "order_id": 1}
    write_to_exchange(exchange, buy_vale)
    write_to_exchange(exchange, sell_bond)
    write_to_exchange(exchange, buy_bond)

    prod_types = ['BOND', 'VALE', 'VALBZ', 'GS', 'MS', 'WFC', 'XLF']
    prod_limits = {}

    live_buy_prices = {}
    live_sell_prices = {}
    
    live_buy_avg = {}
    live_sell_avg = {}

    prod_limits["BOND"] = 100
    prod_limits['VALE'] = 10
    prod_limits['VALBZ'] = 10
    prod_limits['GS'] = 100
    prod_limits['MS'] = 100
    prod_limits['WFC'] = 100
    prod_limits['XLF'] = 100

while True:

    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    
    start = timer()
    while True:
       # if sell and price <= 1k, BUY
       
        message = read_from_exchange(exchange)
        if message["type"] == "book":
            prod = message["symbol"]
            try:
                live_buy_prices[prod] = message['buy'][0][0]
            except IndexError:
                pass

            try:
                live_sell_prices[prod] = message['sell'][0][0]
            except IndexError:
                pass
      
      if message["type"] == "book" and message["symbol"] == "BOND":
        print(message)
      if message["type"] == "fill" or message["type"] == "hello": 
        print(message)

      if message["type"] == "book" and message["symbol"] == "VALE": 
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
