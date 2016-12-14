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
                "twitch_client_key":"",
                "facebook_app_id":""
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
    def __init__(self, service_json):
        self.service_name = service_json['service-name']
        self.channel = service_json['channel']
        self.history = service_json['history']
        self.client_key = config['accounts']['twitch_client_id']
        self.query_url = '{api_url}{channel}?client_id={key}'.format(
                api_url=TWITCH_API_URL,
                channel=self.channel,
                key=config['accounts']['twitch_client_id']
                )
        # gets is_streaming from api.twitch (query_url)
        self.json_data = json.loads(requests.get(self.query_url).text)
        if self.json_data['stream'] is None:
            self.is_streaming = False
        else:
            self.is_streaming = True


class HTML_Update_Service:
    '''for html sites
    '''
    def __init__(self, item):
        self.url = item['url']
        self.service_name = item['service-name']
        self.selector = item['selector']
        self.filt = item['filter']
        self.history = item['history']
        self.soup = bs4.BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.content = self.soup.find_all(attrs=self.selector)
        for item in self.content:
            text = item.get_text()
            if self.filt in text:
                self.requests_text = text
                break

def main():
    magpie = Magpie_Bot()

    for item in config['services']:
        if item['service'] == 'twitch':
            flight = Twitch_Service(item)
            if flight.is_streaming is not flight.history:
                # access item['history'] instead of flight.history
                # in order to change config dict object, so as to
                # write to config.json
                item['history'] = flight.is_streaming
                write_config(config)
                if flight.is_streaming:
                    status_word = 'started'
                else:
                    status_word = 'stopped'
                magpie.post_update('''
<b>{service_name}</b>
{channel} has just {status} streaming
                '''.format(service_name=flight.service_name,
                    channel=flight.channel,
                    status=status_word))
        if item['service'] == 'html':
            flight = HTML_Update_Service(item)
            if not flight.requests_text == flight.history:
                item['history'] = flight.requests_text
                write_config(config)
                magpie.post_update('''
                
<b>{service_name}</b>
{text_body}
                '''.format(service_name=flight.service_name,
                           text_body=flight.requests_text))
                
if __name__ == '__main__':
    main()

