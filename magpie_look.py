'''
magpie_look
'''

import sys
import telegram
import magpie_config, magpie_fetcher

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# CONSTANTS
PATH_SCRIPT = sys.path[0] + '/'
PATH_CONFIG = PATH_SCRIPT + 'config.json'

# INITIALISATION
CONFIG = magpie_config.load()
bot = telegram.Bot(token=CONFIG['accounts']['TELEGRAM_BOT_TOKEN'])
fetcher = magpie_fetcher.Fetcher(bot)
fetcher.chat_id = CONFIG['accounts']['TELEGRAM_CHAT_ID']
fetcher.twitch_client_id = CONFIG['accounts']['TWITCH_CLIENT_ID']

# MAGPIE-FETCHER
for feed in CONFIG['rss']:  # iterate over list of dicts
    if feed['NAME'] != '':
        fetcher.read_rss(feed)
        if fetcher.new_update != fetcher.last_update:
            fetcher.send()
            feed['LAST_UPDATE'] = fetcher.new_update

# UPDATE CONFIG
magpie_config.save(CONFIG)

