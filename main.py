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
PATH_HISTORY_JSON = PATH + 'history.json'
TELEGRAM_CHANNEL_ID_QUERY = '{"ok":false,"error_code":401,"description":"Unauthorized"}'
TWITCH_API_URL = 'https://api.twitch.tv/kraken/streams/'

# CONFIG.JSON
if not os.path.isfile(PATH_CONFIG_JSON):
    with open(PATH_CONFIG_JSON, 'w') as file:
        json.dump(
            {"accounts": {
                "telegram_bot_token":"",
                "telegram_channel_public_link":"",
                "telegram_channel_id":"",
                "twitch_client_key":""
            },
             "services": [
                    {
                       "site":"",
                       "url":""
                    }
                ]
            },
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
            query = self.bot.sendMessage(chat_id=self.channel_public_link, text=TELEGRAM_CHANNEL_ID_QUERY)
            self.channel_id = query.chat.id
            config['accounts']['telegram_channel_id'] = self.channel_id
            write_config(config)
    
    def post_update(self, message):
        self.bot.sendMessage(chat_id=self.channel_id, parse_mode='HTML', text=message)


class Twitch_Service:
    '''for channels on twitch
    '''
    def __init__(self, channel):
        self.channel = channel
        self.client_key = config['accounts']['twitch_client_id']
        self.query_url = '{api_url}{channel}?client_id={key}'.format(
                api_url=TWITCH_API_URL,
                channel=self.channel,
                key=config['accounts']['twitch_client_id']
                )
        self.json_data = json.loads(requests.get(self.query_url).text)
        if self.json_data['stream'] is None:
            self.is_streaming = False
        else:
            self.is_streaming = True


def main():
    magpie = Magpie_Bot()

    for item in config['services']:
        if item['service'] == 'twitch':
            flight = Twitch_Service(item['channel'])
            if flight.is_streaming is not item['history']:
                item['history'] = flight.is_streaming
                write_config(config)
                if flight.is_streaming:
                    status_word = 'started'
                else:
                    status_word = 'stopped'
                magpie.post_update('''
<b>Twitch/{channel}</b>
{channel} has just {status} streaming
                '''.format(channel=item['channel'], status=status_word))
                
if __name__ == '__main__':
    main()

