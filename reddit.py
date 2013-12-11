"""
reddit.py - Reddit Module
Leandro Ardissone, http://iamlee.ch/
"""

from willie.module import commands, example, rate
from willie.web import decode
import praw
from praw.errors import InvalidSubreddit


@commands('reddit', 'r')
@example('.reddit learnpython 2')
@rate(20)
def reddit(bot, trigger):
    """Display posts from reddit"""

    args = trigger.group(2)

    if not args:
        bot.reply('no, vieja: .reddit subreddit [cantidad]')
        return

    args = args.split(' ')

    subreddit = args[0]

    if len(args) == 1:
        limit = 1
    else:
        try:
            limit = int(args[1])
        except ValueError:
            limit = 1

    if limit > 4:
        limit = 4

    r = praw.Reddit(user_agent='Trolo Bot (praw)')

    try:
        subr = r.get_subreddit(subreddit, fetch=True)
    except InvalidSubreddit:
        bot.reply('rofl, ese subreddit no existe, locura!')
        return

    results = subr.get_hot(limit=limit)

    out = 'r/%(subreddit)s: %(title)s [%(ups)s/%(downs)s] %(url)s [%(short_link)s]'
    for r in results:
        output = out % {
            'subreddit': r.subreddit,
            'title': decode(r.title),
            'ups': r.ups,
            'downs': r.downs,
            'url': r.url,
            'short_link': r.short_link
        }
        bot.say(output)
