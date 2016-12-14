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

# config.json
if not os.path.isfile(PATH_CONFIG_JSON):
    with open(PATH_CONFIG_JSON, 'w') as file:
        json.dump(
            {"accounts":
                {"telegram_bot_token":"",
                 "telegram_channel_name":"",
                 "telegram_channel_id":""},
             "services":
                {"site":"",
                 "url":""}},
            file,
            indent=4
        )
with open(PATH_CONFIG_JSON, 'r') as file:
    raw_json_string = file.read()
    json_config = json.loads(raw_json_string)

'''
class web_grabber:
    def __init__():
        self.url = 'https://www.facebook.com/pg/UberSingapore/posts/'
        self.html = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.html.text, 'html.parser')
        self.pbx_list = self.soup.find_all('div', {'class':'_5pbx userContent'})
        self.p_list = []
        for item in self.pbx_list:
            if item.p.string is not None:
                self.p_list.append(item.p.string)
'''