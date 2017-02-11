import json
import requests, telegram
import magpie.core

class Twitch(magpie.core.Core):
    '''
    Twitch handles all interactions with the twitch kraken api.
    It inherits from the class Core.
    '''
    API_ADDRESS = 'https://api.twitch.tv/kraken/streams/{}?client_id={}'

    def __init__(self):
        magpie.core.Core.__init__(self)
        self.client_id = self.config['twitch']['client_id']
        self.following = self.config['twitch']['following']

    def send_updates(self):
        standby_message = self.send_me('Standby...')
        standby_message.edit_text(self.build_updates(), parse_mode=telegram.ParseMode.HTML)

    def build_updates(self):
        statuses = {'online': [], 'offline': []}
        for channel in self.following:
            status = self.build_update(channel)
            if 'offline' in status:
                statuses['offline'].append(status)
            else:
                statuses['online'].append(status)

        updates_body = '<b>Twitch Streams</b>\n'
        for status in statuses['online']:
            updates_body += status
        for status in statuses['offline']:
            updates_body += status
        return updates_body

    def build_update(self, channel):
        stream_status = self.retrieve_update(channel['channel_name'])
        if stream_status is None:
            channel['last_update'] = stream_status
            Twitch.save_config(self.config)
            return '{} is offline\n'.format(channel['streamer'])
        else:
            channel['last_update'] = stream_status
            Twitch.save_config(self.config)
            return '{} is online with <i>{}</i>\n'.format(channel['streamer'], stream_status)

    def retrieve_update(self, channel_name):
        raw_page = requests.get(Twitch.API_ADDRESS.format(channel_name, self.client_id))
        raw_json = raw_page.text
        stream_data = json.loads(raw_json)
        if stream_data['stream'] is None:
            return None
        else:
            return stream_data['stream']['game']

