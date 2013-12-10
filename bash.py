"""
bash.py - Quotes from bash and qdb
Leandro Ardissone, http://iamlee.ch/
"""

import willie
from willie import web
import re
import random


class Bash(object):

    random = u'http://www.bash.org/?random'
    bynum = u'http://www.bash.org/?num'
    search = u'http://www.bash.org/'
    query = 'search'
    opts = dict(show=100)
    entries = re.compile(u'<p class="qt">(.*?)</p>', re.DOTALL)


class QDB(object):

    random = 'http://qdb.us/random'
    bynum = 'http://qdb.us/num'
    search = 'http://qdb.us/'
    query = 'search'
    opts = dict(limit=100, approved=1)
    entries = re.compile(r'<span class=qt[^>]*>(.*?)</span>', re.DOTALL)


@willie.module.commands('bash', 'qdb')
@willie.module.rate(20)
@willie.module.priority('low')
def bash(bot, trigger):
    source = None

    if str(trigger) == '.bash':
        source = Bash()
    elif str(trigger) == '.qdb':
        source = QDB()

    if source:
        try:
            query = trigger.group(2).strip()
        except:
            query = None
        try:
            num = int(query)
            query = None
        except:
            num = None
        if num:
            url = source.bynum.replace(u'num', unicode(num))
            opts = None
        elif query:
            url = source.search
            opts = dict(source.opts)
            opts[source.query] = query
        else:
            url = source.random
            opts = None

        page = web.get(url)
        entries = source.entries.findall(page)

        if query:
            entries = filter(None, entries)

        entry = random.choice(entries)
        for line in HTMLStripper(entry).stripped.strip().splitlines():
            bot.say(line)


# TODO: reuse this thing
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
name2codepoint = dict(name2codepoint)
name2codepoint['apos'] = ord("'")
class HTMLStripper(HTMLParser):

    def __init__(self, data):
        HTMLParser.__init__(self)
        self._stripped = []
        self.feed(data)

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'br':
            self._stripped.append('\n')

    def handle_charref(self, name):
        try:
            if name.lower().startswith('x'):
                char = int(name[1:], 16)
            else:
                char = int(name)
            self._stripped.append(unichr(char))
        except Exception, error:
            log.warn('invalid entity: %s' % error)

    def handle_entityref(self, name):
        try:
            char = unichr(name2codepoint[name])
        except Exception, error:
            log.warn('unknown entity: %s' % error)
            char = u'&%s;' % name
        self._stripped.append(char)

    def handle_data(self, data):
        self._stripped.append(data)

    @property
    def stripped(self):
        return ''.join(self._stripped)
