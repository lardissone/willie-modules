# -*- coding: UTF-8 -*-
"""
bardero.py - Module to annoy people
Leandro Ardissone, http://iamlee.ch/
"""

from willie.module import rule
from random import choice

@rule('.*(hola|hi|buenas).*')
def hi(bot, trigger):
    replies = [
        ('reply', u'hola, fagget!'),
        ('msg', u'llegó el putito!'),
        ('reply', u'hola, bananero!!'),
        ('msg', u'habran cancha que alguien está feliz, que le habrán hecho!?'),
        ('reply', u'hola a tu vieja!'),
    ]
    output = choice(replies)
    if (output[0] == 'reply'):
        bot.reply(unicode(output[1]))
    else:
        bot.say(unicode(output[1]))
