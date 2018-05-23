import configparser, logging

import core

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

bot = core.Bot(
    token=config['telegram']['token'], 
    admin_id=config['telegram']['admin_id'])
bot.send_me('<code>Poo-tee-weet?</code>')
bot.listen()
