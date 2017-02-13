import feedparser, telegram
import magpie.core

class Rss(magpie.core.Core):
    '''
    Rss handles interactions with rss feeds through the feedparser library.
    It inherits from the class Core.
    '''
    update_body = '<b>{}</b>\n{}'

    def __init__(self):
        magpie.core.Core.__init__(self)
        self.following = self.config['rss']['following']

    def send_new_updates(self):
        for feed in self.following:
            this_update = self.retrieve_update(feed['url'])
            if this_update != feed['last_update']:
                feed['last_update'] = this_update
                self.save_config(self.config)
                self.send_me(self.build_update(feed))

    def build_update(self, feed):
        return self.update_body.format(feed['name'], feed['last_update'])

    def retrieve_update(self, feed_url):
        feed_content = feedparser.parse(feed_url)
        return feed_content['entries'][0]['link']

