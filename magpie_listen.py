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
    bot.send_message(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,  # redun.
            text='Standby...'
            )
    status_body = '<b>Twitch Streams</b>\n'

    for feed in CONFIG['twitch']:
        fetcher.read_kraken(feed)
        if fetcher.new_update is False:
            # stream is offline
            status_body += '{} is offline\n'.format(
                    fetcher.name
            )
        else:
            # stream is online
            status_body += '{} is online with <i>{}</i>\n'.format(
                    fetcher.name,
                    fetcher.new_update
            )

        feed['LAST_UPDATE'] = fetcher.new_update  # redun.
    magpie_config.save(CONFIG) # redun.

    bot.send_message(
            chat_id=CONFIG['accounts']['TELEGRAM_CHAT_ID'],
            parse_mode=telegram.ParseMode.HTML,
            text=status_body
            )

def media_upload(bot, update):
    file_id = sync.get_file_id(update)
    sync.download(file_id, CONFIG['accounts']['SYNC_DIR'])
    bot.send_message(
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

