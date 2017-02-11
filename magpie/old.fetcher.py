'''
magpie_fetcher
'''

import json
import feedparser, telegram, requests

class Fetcher:
    '''
    Handle interactions with external web services (e.g. RSS, twitch)

    Information is 'got' through the read methods (i.e. read_rss, read_kraken)
    Thereafter retrieved information is saved in instance variables
    And should be accessed through Fetcher.attribute
    '''

    def __init__(self, bot):
        '''
        Initiate fetcher with telegram.Bot

        Creates instance variables and uses None as placeholder
        until a read_rss or read_kraken method is called
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
        Read from RSS and save in instance variables

        ARGUMENTS:
        feed_config: dict containing RSS info

        Uses feedparser to retrieve RSS updates
        Saves updates in this object's instance variables
        '''
        # retrieve from feed_config
        self.name = feed_config['NAME']
        self.url = feed_config['URL']
        self.last_update = feed_config['LAST_UPDATE']
        # retrieve from feedparser
        feed = feedparser.parse(self.url)
        self.new_update = feed['entries'][0]['link']

    def read_kraken(self, channel_config):
        '''
        Read from api.twitch.tv/kraken and save in instance variables

        ARGUMENTS:
        channel_config: dict containing twitch info

        Uses requests, json.loads to retrieve kraken's json
        Saves info in this object's instance variables
        '''
        # retrieve from channel_config
        self.name = channel_config['NAME']
        self.url = channel_config['URL']
        self.last_update = channel_config['LAST_UPDATE']  # redundant
        # retrieve from kraken
        URL_KRAKEN = 'https://api.twitch.tv/kraken/streams/'
        url_query = '{KRAKEN}{channel}?client_id={key}'.format(
                KRAKEN=URL_KRAKEN,
                channel=self.url,
                key=self.twitch_client_id
                )
        json_data = json.loads(requests.get(url_query).text)
        if json_data['stream'] is None:
            # stream is offline
            self.new_update = None
        else:
            # stream is online
            self.new_update = json_data['stream']['game']

    def send(self):
        '''
        Send telegram message about new update

        Takes these required information from instance:
        (1) chat_id: chat to send update to
        (2) new_update: what the new update is

        Since this method does not take the required info
        as arguments, but as instance variables, the fetcher
        object needs to be properly initiated with the required
        values before calling this send() method.
        '''
        if self.chat_id == None:
            raise NoChatIdException  # redun.
        else:
            self.bot.send_message(chat_id=self.chat_id, 
                    parse_mode=telegram.ParseMode.HTML,
                    text='<b>{}</b>\n{}'.format(self.name, self.new_update))

class NoChatIdException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

