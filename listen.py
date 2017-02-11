import telegram, telegram.ext
import magpie.core, magpie.twitch

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# INITIALISATION
core    = magpie.core.Core()
twitch  = magpie.twitch.Twitch()
updater = telegram.ext.Updater(bot=core.bot)

# BOT FUNCTIONS
def command_help(bot, update):
    this_chat_id = update.message.chat_id
    if core.is_my_chat_id(this_chat_id):
        core.send_me('''
<b>Commands</b>
<code>/streams</code> - Statuses of all streams
<code>/streamson</code> - Realtime updates ON
<code>/streamsoff</code> - Realtime updates OFF
<code>/help</code> - This help message
''')
    else:
        core.send_me('<b>{} ATTEMPTED TO USE BOT</b>'.format(this_chat_id))

def command_streams(bot, update):
    this_chat_id = update.message.chat_id
    if core.is_my_chat_id(this_chat_id):
        twitch.send_updates()
    else:
        core.send_me('<b>{} ATTEMPTED TO USE BOT</b>'.format(this_chat_id))

help_handler = telegram.ext.CommandHandler('help', command_help)
updater.dispatcher.add_handler(help_handler)

streams_handler = telegram.ext.CommandHandler('streams', command_streams)
updater.dispatcher.add_handler(streams_handler)

updater.start_polling()

