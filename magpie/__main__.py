import configparser, logging

import core

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

bot = core.Bot(config['telegram']['token'], config['telegram']['my_id'])
bot.send_me('<code>Poo-tee-weet?</code>')
bot.listen()
