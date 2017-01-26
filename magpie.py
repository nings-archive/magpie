# inbuilts
import os, sys, json
# externals
import telegram
# locals
import magpie_sync, magpie_fetcher

# CONSTANTS
PATH_SCRIPT = sys.path[0] + '/'
PATH_CONFIG = PATH_SCRIPT + 'config.json'

# CONFIG (config.json)
if not os.path.isfile(PATH_CONFIG):
    with open(PATH_CONFIG, 'w') as file:
        json.dump(
{
    'accounts': {
        'TELEGRAM_BOT_TOKEN': '',
        'TELEGRAM_CHAT_ID': '',
        'SYNC_DIR': ''
    },
    'rss': (
        {
            'NAME': '',
            'URL': '',
            'LAST_UPDATE': ''
        },
    )
},
            file,
            indent=4
        )
    sys.exit(0)
with open(PATH_CONFIG, 'r') as file:
    CONFIG = json.loads(file.read())

# INITIALISATION
bot = telegram.Bot(CONFIG['accounts']['TELEGRAM_BOT_TOKEN'])
sync = magpie_sync.Sync(bot)
fetcher = magpie_fetcher.Fetcher(bot)
fetcher.chat_id = CONFIG['accounts']['TELEGRAM_CHAT_ID']  # bad prac?

# MAGPIE-SYNC
count_downloads = 0
for update in sync.new_updates():
    file_id = sync.get_file_id(update)
    if file_id != None:
        count_downloads += 1
        sync.download(file_id, config.SYNC_DIR)
if count_downloads != 0:  # notify of downloads
    bot.send_message(chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parsemode=telegram.ParseMode.HTML,  # redundant, tbh
            text='Success! {} files uploaded.'.format(count_downloads))

# MAGPIE-FETCHER
for feed in CONFIG['rss']:  # iterate over array of dicts (list)
    if feed['NAME'] != '':
        fetcher.read_rss(feed)
        if fetcher.new_update != fetcher.last_update:
            fetcher.send()
            feed['LAST_UPDATE'] = fetcher.new_update

# UPDATE CONFIG
with open(PATH_CONFIG, 'w') as file:
    json.dump(CONFIG, file, indent=4)

