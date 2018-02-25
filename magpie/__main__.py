import configparser
from bot import Bot

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(config['telegram']['token'], config['telegram']['my_id'])
bot.send_me('Hello world!')
