# Magpie
# ningyuan.sg@gmail.com
# Telegram: Magpie, @PicaApparatusBot  #rm-mark

import sys, os, logging, time, json, csv
import requests, bs4

# CONSTANTS
PATH = sys.path[0] + "/"
PATH_CONFIG_JSON = PATH + "config.json"

# config.json
if not os.path.isfile(PATH_CONFIG_JSON):
    with open(PATH_CONFIG_JSON, "w") as file:
              file.write(
"""{
  "accounts":
      {
          "telegram":""
      },
  "services":
      {
          "site":"",
          "url":"",
          "selector":""
      }
}"""
              )
with open(PATH_CONFIG_JSON, "r") as file:
    raw_json_string = file.read()
    json_config = json.loads(raw_json_string)

class web_grabber:
    '''Handles interactions with facebook html.
    '''
    def __init__():
        self.url = 'https://www.facebook.com/pg/UberSingapore/posts/'
        self.html = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.html.text, 'html.parser')
        self.pbx_list = self.soup.find_all('div', {'class':'_5pbx userContent'})
        self.p_list = []
        for item in self.pbx_list:
            if item.p.string is not None:
                self.p_list.append(item.p.string)

