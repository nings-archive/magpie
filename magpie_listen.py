'''
magpie_listen
'''

import telegram, telegram.ext
import magpie_config, magpie_fetcher, magpie_sync

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# INITIALISATION
CONFIG = magpie_config.load()
bot = telegram.Bot(token=CONFIG['accounts']['TELEGRAM_BOT_TOKEN'])
updater = telegram.ext.Updater(token=CONFIG['accounts']['TELEGRAM_BOT_TOKEN'])
fetcher = magpie_fetcher.Fetcher(bot)
fetcher.chat_id = CONFIG['accounts']['TWITCH_CLIENT_ID']
fetcher.twitch_client_id = CONFIG['accounts']['TWITCH_CLIENT_ID']
sync = magpie_sync.Sync(bot)

# BOT FUNCTIONS
def stream_status(bot, update):
    '''
    Send message detailing status of streams in CONFIG

    ARGUMENTS
    bot, update: required args for telegram.ext.CommandHandler

    Passes each dict in list CONFIG['twitch'] to fetcher,
    appends a line for each dict (i.e. channel) accordingly.
    '''
    # Load config, send standby message
    CONFIG = magpie_config.load()
    message_standby = bot.send_message(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,  # redun.
            text='Standby...'
            )

    stream_status = {
            'offline': [],
            'online' : []
    }

    # Check feeds, stash in stream_status dict, update CONFIG, config.json
    for feed in CONFIG['twitch']:
        fetcher.read_kraken(feed)
        if fetcher.new_update is None:
            # stream is offline
            stream_status['offline'].append('{} is offline\n'.format(
                    fetcher.name
            ))
        else:
            # stream is online
            stream_status['online'].append('{} is online with <i>{}</i>\n'.format(
                    fetcher.name,
                    fetcher.new_update
            ))
        feed['LAST_UPDATE'] = fetcher.new_update  # redun.
    magpie_config.save(CONFIG) # redun.

    # Build body text (onlines first, then offlines)
    status_body = '<b>Twitch Streams</b>\n'
    for line in stream_status['online']:
        status_body += line
    for line in stream_status['offline']:
        status_body += line

    message_standby.edit_text(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,
            text=status_body
            )

def media_upload(bot, update):
    '''
    Uploads media file of update to specified directory in CONFIG

    ARGUMENTS
    bot, update: required args for telegram.ext.MessageHandler

    Uses sync (magpie_sync.Sync) methods to download media contained
    in update into directory specified in CONFIG['accounts']['SYNC_DIR']
    '''
    message_standby = bot.send_message(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,  # redun.
            text='Standby...'
    )
    CONFIG = magpie_config.load()
    file_id = sync.get_file_id(update)
    sync.download(file_id, CONFIG['accounts']['SYNC_DIR'])
    message_standby.edit_text(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,  # redun.
            text='File uploaded!'
    )

twitch_handler = telegram.ext.CommandHandler('streams', stream_status)
updater.dispatcher.add_handler(twitch_handler)

upload_handler = telegram.ext.MessageHandler(
        (telegram.ext.Filters.audio |
         telegram.ext.Filters.document |
         telegram.ext.Filters.photo |
         telegram.ext.Filters.video |
         telegram.ext.Filters.voice),
        media_upload)
updater.dispatcher.add_handler(upload_handler)

updater.start_polling()

