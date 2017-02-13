import telegram, telegram.ext
import magpie.core, magpie.twitch

# DEBUG
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# INITIALISATION
core    = magpie.core.Core()
twitch  = magpie.twitch.Twitch()

# TWITCH
if twitch.realtime_enabled:
    twitch.send_new_updates()

