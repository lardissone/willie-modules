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


def _dolar_blue(jenni):
    """get blue dollar exchange in ARS"""

    r = requests.get('http://www.eldolarblue.net/getDolarBlue.php?as=json')
    if r.status_code == 200:
        # assholes didn't formatted JSON well
        regex = re.compile("exchangerate:\\{buy:(.{0,}),sell:(.{0,})\\}\\}")
        matchArray = regex.findall(r.text)
        jenni.say('[DOLAR BLUE]: compra: $%s - venta: $%s' % (matchArray[0][0], matchArray[0][1]))
    else:
        jenni.reply('sorry vieja, no me anda el we\'servis del blue...')

def _dolar(jenni):
    """get dollar exchange in ARS"""

    r = requests.get('http://www.eldolarblue.net/getDolarLibre.php?as=json')
    if r.status_code == 200:
        # assholes didn't formatted JSON well
        regex = re.compile("exchangerate:\\{buy:(.{0,}),sell:(.{0,})\\}\\}")
        matchArray = regex.findall(r.text)
        jenni.say('[DOLAR]: compra: $%s - venta: $%s' % (matchArray[0][0], matchArray[0][1]))
    else:
        jenni.reply('sorry vieja, no me anda el we\'servis del dolar...')


def _bitcoin(jenni):
    """get bitcoin exchange in USD"""

    r = requests.get('https://blockchain.info/es/ticker')
    if r.status_code == 200:
        data = r.json()
        jenni.say('[BITCOIN]: compra: USD %s - venta: USD %s' % (
            data['USD']['buy'],
            data['USD']['sell'],
        ))
    else:
        jenni.reply('sorry vieja, no me anda el we\'servis del bitcoin...')

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
