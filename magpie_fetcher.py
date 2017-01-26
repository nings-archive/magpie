'''
magepie_fetcher
'''

import telegram, feedparser

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

