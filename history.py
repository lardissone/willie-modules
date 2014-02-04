#!/usr/bin/env python
"""
Hoy en la historia

Source: web de History Channel

Requires: requests and BeautifulSoup4
"""

from random import choice
import requests
import willie
from bs4 import BeautifulSoup


@willie.module.commands('history', 'today')
def history(bot, input):
    """ returns a random fact of the history for today """

    r = requests.get('http://mx.tuhistory.com/hoy-en-la-historia.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)

        soup = soup.find_all('div', class_='cont_box_pie2')[0]
        soup = soup.find_all('div', class_='cont_box_bg2')[0]

        items = soup.find_all('div', recursive=False)
        item = choice(list(items))
        title = item.find_all('h3')[0]
        date = item.find_all('b')[0]

        text = 'Hoy en la historia: [%s] %s' % (
            date.string,
            title.string
        )
        bot.say(text)
    else:
        bot.reply('sorry vieja, no anduvo, vivi el presente...')

history.commands = ['history', 'today']
history.example = ".history"

if __name__ == '__main__':
    print __doc__.strip()
