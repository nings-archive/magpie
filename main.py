# Magpie
# ningyuan.sg@gmail.com
# Telegram: Magpie, @PicaApparatusBot  #rm-mark

import sys, os, logging, time, json, csv
import telegram
import requests, bs4

# LOGGING
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# CONSTANTS
PATH = sys.path[0] + '/'
PATH_CONFIG_JSON = PATH + 'config.json'
CHANNEL_ID_QUERY = '{"ok":false,"error_code":401,"description":"Unauthorized"}'

# CONFIG.JSON
if not os.path.isfile(PATH_CONFIG_JSON):
    with open(PATH_CONFIG_JSON, 'w') as file:
        json.dump(
            {"accounts":
                {"telegram_bot_token":"",
                 "telegram_channel_public_link":"",
                 "telegram_channel_id":""},
             "services":
                {"site":"",
                 "url":""}},
            file,
            indent=4
        )
with open(PATH_CONFIG_JSON, 'r') as file:
    raw_json_string = file.read()
    config = json.loads(raw_json_string)
    
def write_config(config):
    with open(PATH_CONFIG_JSON, 'w') as file:
        json.dump(config, file, indent=4)

# CLASSES
class Magpie_Bot:
    '''magpie is the class for the telegram api
    '''
    def __init__(self):
        self.token = config['accounts']['telegram_bot_token']
        self.bot = telegram.Bot(token=self.token)
        self.channel_public_link = config['accounts']['telegram_channel_public_link']
        self.channel_id = config['accounts']['telegram_channel_id']
        if self.channel_id == '':
            query = self.bot.sendMessage(chat_id=self.channel_public_link, text=CHANNEL_ID_QUERY)
            self.channel_id = query.chat.id
            config['accounts']['telegram_channel_id'] = self.channel_id
            write_config(config)

magpie = Magpie_Bot()
