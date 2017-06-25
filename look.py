#!/usr/bin/env python3
import telegram, telegram.ext
import magpie.core, magpie.twitch, magpie.rss, magpie.dota2

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# TWITCH
twitch = magpie.twitch.Twitch()
if twitch.realtime_enabled:
    twitch.send_new_updates()

# RSS
rss = magpie.rss.Rss()
rss.send_new_updates()

# DOTA2
dota2   = magpie.dota2.Dota2()
dota2.send_latest_match()

