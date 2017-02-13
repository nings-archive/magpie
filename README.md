# Magpie
Magpie is a [telegram](https://telegram.org/) bot that serves to provide utility through the messaging app (and thus mobile phone). Among other things, it functions as a notification center for web content. 

At it's core, Magpie is an implementation of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) along with some other external modules.

## config.json

```
config.json
    |
    +--dict: core
    |      + str: token
    |      + str: dl_dir
    |      + str: chat_id
    +--dict: rss
    |      + list: following
    |            + str: name
    |            + str: url
    |            + str: last_update
    +--dict: twitch
           + str: client_id
           + bool: realtime
           + list: following
                 + str: streamer
                 + str: channel_name
                 + str/None: game
```
