#!/usr/bin/env python
"""
Stock quotes

Requires: requests
"""

import re
import requests
import willie


@willie.module.commands('stock')
def stock(bot, input):
    """stocks quotes"""
    symbol = input.group(2)
    if not symbol:
        return bot.reply("ponete algun stock symbol")

    symbol = symbol.strip()

    query = "select * from yahoo.finance.quotes where symbol in ('%s')" % symbol
    data = {'q': query, 'format': 'json', 'diagnostics': True, 'env': 'http://datatables.org/alltables.env'}
    r = requests.get('http://query.yahooapis.com/v1/public/yql', params=data)

    if r.status_code == 200:
        response = r.json()

        if response['query']['count'] > 0:
            bot.say('[%s]: $%s' % (
                response['query']['results']['quote']['symbol'],
                response['query']['results']['quote']['LastTradePriceOnly']
            ))
        else:
            bot.reply('estas seguro que existe el symbol "%s"' % symbol)
    else:
        bot.reply('algo no anduvo, vaya a laburar...')

stock.commands = ['stock']
stock.example = ".stock GOOG"

if __name__ == '__main__':
    print __doc__.strip()
