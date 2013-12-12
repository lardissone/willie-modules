# -*- coding: UTF-8 -*-
"""
quotes.py - Quotes module

Needs MongoDB, and added the section in the config file like:

    [mongodb]
    uri = "mongodb://user:pass@host:port/database"

Leandro Ardissone, http://iamlee.ch/
"""


from willie.module import rule, priority, rate, commands
from random import randint


try:
    from pymongo import MongoClient
except ImportError:
    bot.say('Install mongo lib: pip install mongo')


@commands('addquote')
@rate(20)
@priority('low')
def addquote(bot, trigger):
    """ add quote to channel """
    if trigger.sender.startswith('#'):
        quote = trigger.group(2)

        if quote and len(quote):
            db = _get_db(bot)
            db.quotes.save({
                'channel': trigger.sender,
                'quote': quote
                })

            bot.say('Agregada la quote!')
        else:
            bot.reply(unicode(u'Y la quote, papá?'))

    else:
        bot.reply('Nope, solo en un canal van los quotes')


@commands('quote')
@rate(20)
@priority('low')
def quote(bot, trigger):
    """ get random quote """
    if trigger.sender.startswith('#'):
        channel = trigger.sender
        args = trigger.group(2)

        pos = None
        if args:
            args = args.split(' ')
            # specific quote
            try:
                pos = int(args[0])
            except ValueError:
                pos = None

        db = _get_db(bot)
        total_quotes = db.quotes.find({'channel': channel}).count()

        if total_quotes == 0:
            bot.reply('No tenemo\' quotes pa\' este channel')
            return

        if not pos:
            # random quote
            pos = randint(0, total_quotes-1)

        quote = db.quotes.find({'channel': channel}).skip(pos).next()

        if quote:
            bot.say('[QUOTE] [%s/%s]: %s' % (pos+1, total_quotes, quote['quote']))

        print quote

    else:
        bot.reply('Nope, solo en un canal van los quotes')


def setup(bot):
    config = bot.config
    if not config.has_section('mongodb') or not config.mongodb.uri:
        bot.say('Todo mal, te faltan los settings de MongoDB en la db')

def _get_db(bot):
    mongo = MongoClient(bot.config.mongodb.uri)
    db = mongo.get_default_database()
    return db
