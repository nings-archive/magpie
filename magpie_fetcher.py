'''
magpie_fetcher
'''

import json
import feedparser, telegram, requests

class Fetcher:
    def __init__(self, bot):
        '''
        initiate with telegram.Bot obj
        '''
        self.bot = bot
        self.name = None
        self.url = None
        self.last_update = None
        self.new_update = None
        # must be assigned manually. bad?
        self.chat_id = None
        self.twitch_client_id = None

    def read_rss(self, feed_config):
        '''
        edit instance variables to this feed
        feed_config: dict
        '''
        # read from CONFIG
        self.name = feed_config['NAME']
        self.url = feed_config['URL']
        self.last_update = feed_config['LAST_UPDATE']
        # read from RSS
        feed = feedparser.parse(self.url)
        self.new_update = feed['entries'][0]['link']

    def read_kraken(self, channel_config):
        '''
        edit instance variables to kraken response
        channel_config: dict
        '''
        self.name = channel_config['NAME']
        self.url = channel_config['URL']
        self.last_update = channel_config['LAST_UPDATE']  # redundant
        URL_KRAKEN = 'https://api.twitch.tv/kraken/streams/'
        url_query = '{KRAKEN}{channel}?client_id={key}'.format(
                KRAKEN=URL_KRAKEN,
                channel=self.url,
                key=self.twitch_client_id
                )
        json_data = json.loads(requests.get(url_query).text)
        if json_data['stream'] is None:
            self.new_update = False
        else:
            self.new_update = json_data['stream']['game']
        


    def send(self):
        '''
        sends message with self.new_update
        '''
        if self.chat_id == None:
            raise NoChatIdException
        else:
            self.bot.send_message(chat_id=self.chat_id, 
                    parse_mode=telegram.ParseMode.HTML,
                    text='<b>{}</b>\n{}'.format(self.name, self.new_update))

class NoChatIdException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

