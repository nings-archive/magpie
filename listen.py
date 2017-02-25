import telegram, telegram.ext
import magpie.core, magpie.twitch

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# INITIALISATION
core    = magpie.core.Core()
twitch  = magpie.twitch.Twitch()
updater = telegram.ext.Updater(bot=core.bot)

# BOT FUNCTIONS
# im sure theres some way to DRY the chat_id authentication
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
        twitch.__init__()
        twitch.mt_send_all_updates()
    else:
        core.send_me('<b>{} ATTEMPTED TO USE BOT</b>'.format(this_chat_id))

def command_streamson(bot, update):
    this_chat_id = update.message.chat_id
    if core.is_my_chat_id(this_chat_id):
        twitch.__init__()
        twitch.toggle_realtime(True)
        twitch.send_toggle_state()
    else:
        core.send_me('<b>{} ATTEMPTED TO USE BOT</b>'.format(this_chat_id))

def command_streamsoff(bot, update):
    this_chat_id = update.message.chat_id
    if core.is_my_chat_id(this_chat_id):
        twitch.__init__()
        twitch.toggle_realtime(False)
        twitch.send_toggle_state()
    else:
        core.send_me('<b>{} ATTEMPTED TO USE BOT</b>'.format(this_chat_id))

# HANDLER/DISPATCHER
help_handler       = telegram.ext.CommandHandler('help', command_help)
streams_handler    = telegram.ext.CommandHandler('streams', command_streams)
streamson_handler  = telegram.ext.CommandHandler('streamson', command_streamson)
streamsoff_handler = telegram.ext.CommandHandler('streamsoff', command_streamsoff)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(streams_handler)
updater.dispatcher.add_handler(streamson_handler)
updater.dispatcher.add_handler(streamsoff_handler)

updater.start_polling()

