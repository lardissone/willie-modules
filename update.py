"""
update.py - Module to update modules directory
Leandro Ardissone, http://iamlee.ch/
"""

import sys
import subprocess
import willie


if sys.version_info >= (2, 7):
    @willie.module.nickname_commands('updatemodules')
    def update(bot, trigger):
        if not trigger.admin:
            return

        """Pulls the latest versions of all modules from Git"""
        proc = subprocess.Popen('cd /root/.willie/modules && /usr/bin/git pull',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        bot.reply(proc.communicate()[0])
else:
    @willie.module.nickname_commands('update')
    def update(bot, trigger):
        bot.say('You need to run me on Python 2.7 to do that.')
