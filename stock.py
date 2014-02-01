#!/usr/bin/env python
"""
Stock quotes

Requires: requests
"""

import re
import requests
import StringIO
import csv
import willie


@willie.module.commands('stock')
def stock(bot, input):
    """stocks quotes"""
    symbol = input.group(2)
    if not symbol:
        return bot.reply("ponete algun stock symbol")

    symbol = symbol.strip()

    tags = 'nsac' # 'kqwxyr1l9t5p4'
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, tags)

    r = requests.get(url)
    if r.status_code == 200:
        f = StringIO.StringIO(r.text)
        reader = csv.reader(f)

        result = list(reader)[0]

        if result[2] != 'N/A':
            bot.say('%s (%s): $%s (%s)' % (
                result[0],
                result[1],
                result[2],
                result[3]
            ))
        else:
            bot.reply('nope, no tenemos de eso')
    else:
        bot.reply('algo no anduvo, anda a laburar...')

stock.commands = ['stock']
stock.example = ".stock GOOG"

if __name__ == '__main__':
    print __doc__.strip()
