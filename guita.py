#!/usr/bin/env python
"""
Comando de monedas

Web services: http://www.eldolarblue.net/dolar-blue-web-services.php

Gran parte choreado de pungabot por @reiven:
https://github.com/reiven/pungabot/

Requires: requests
"""

import re
import requests
import willie
from bs4 import BeautifulSoup


def _dolar_blue(bot):
    """get blue dollar exchange in ARS"""

    r = requests.get('http://www.ambito.com/economia/mercados/monedas/dolar/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)

        soup = soup.find_all('div', class_='columna3')[0]
        blue = soup.find_all('big')

        text = '[DOLAR BLUE]: compra $%s - venta $%s (actualizado: %s - variacion: %s)' % (
            blue[1].string,
            blue[2].string,
            blue[3].string,
            blue[0].string
        )
        bot.say(text)
    else:
        bot.reply('sorry vieja, no me anda el we\'servis del blue...')

def _dolar(bot):
    """get dollar exchange in ARS"""

    r = requests.get('http://www.ambito.com/economia/mercados/monedas/dolar/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)

        soup = soup.find_all('div', class_='columna1')[0]
        print soup
        dolar = soup.find_all('big')

        print dolar

        text = '[DOLAR]: compra $%s - venta $%s (actualizado: %s - variacion: %s)' % (
            dolar[1].string,
            dolar[2].string,
            dolar[3].string,
            dolar[0].string
        )
        bot.say(text)
    else:
        bot.reply('sorry vieja, no me anda el we\'servis del dolar...')


def _bitcoin(bot):
    """get bitcoin exchange in USD"""

    r = requests.get('https://blockchain.info/es/ticker')
    if r.status_code == 200:
        data = r.json()
        bot.say('[BITCOIN]: compra: USD %s - venta: USD %s' % (
            data['USD']['buy'],
            data['USD']['sell'],
        ))
    else:
        bot.reply('sorry vieja, no me anda el we\'servis del bitcoin...')

@willie.module.commands('guita')
def guita(bot, input):
    """currencies checker"""
    moneda = input.group(2)
    if not moneda:
        return bot.reply("que moneda queres chequear? (dolar, blue, bitcoin)")

    moneda = moneda.strip()

    if moneda == 'dolar':
        _dolar(bot)
    elif moneda == 'blue':
        _dolar_blue(bot)
    elif moneda == 'bitcoin':
        _bitcoin(bot)
    else:
        bot.reply('no, vieja.. Le pifiaste de moneda: dolar, blue o bitcoin..')

guita.commands = ['guita']
guita.example = ".guita dolar"

if __name__ == '__main__':
    print __doc__.strip()
