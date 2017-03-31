import telegram, dota2api
import magpie.core

class Dota2(magpie.core.Core):
    '''
    Dota2 handles interactions with the external module dota2api
    It inherits from the class Core.
    '''
    OPENDOTA_ADDRESS = 'http://www.opendota.com/matches/{}'
    RADIANT_SLOTS = {'0', '1', '2', '3', '4'}
    DIRE_SLOTS    = {'128', '129', '130', '131', '132'}

    def __init__(self):
        magpie.core.Core.__init__(self)
        self.api_key    = str(self.config['dota2']['api_key'])
        self.steam_id   = str(self.config['dota2']['steam_id'])
        self.last_match = str(self.config['dota2']['last_match'])
        self.api        = dota2api.Initialise(self.api_key)

    def send_latest_match(self):
        latest_match_id = self.retrieve_latest_match_id()
        if latest_match_id != self.last_match:
            self.config['dota2']['last_match'] = latest_match_id
            Dota2.save_config(self.config)
            self.send_me(self.build_latest_match_message(latest_match_id))

    def build_latest_match_message(self, match_id):
        match_json  = self.retrieve_match_json(match_id)
        player_json = self.my_player(match_json)
        my_kda      = self.my_kda(player_json)
        my_kda_f    = '{}/{}/{}'.format(my_kda[0], my_kda[1], my_kda[2])
        my_hero     = self.my_hero(player_json)
        my_team     = self.my_team(player_json)
        my_duration = self.my_game_duration(match_json)
        radiant_win = self.my_game_radiant_win(match_json)
        my_win      = self.my_win_or_lose(my_team, radiant_win)
        return '''
<b>{hero} [{kda}]</b>
{time} - {winloss}
{opendota}
'''.format(hero=my_hero[1], kda=my_kda_f,
        time=self.format_time(my_duration),
        winloss=my_win,
        opendota=self.OPENDOTA_ADDRESS.format(match_id))

    @staticmethod
    def format_time(time_in_s):
        '''
        int:time_in_s -> str:formatted_time
        '''
        minutes = time_in_s // 60
        seconds = time_in_s % 60
        # following fixes single digit seconds e.g. 32m2s -> 32:2
        seconds = str(seconds)
        if len(seconds) == 1:
            seconds = '0' + seconds
        return '{}:{}'.format(minutes, seconds)

    def my_win_or_lose(self, my_team, radiant_win):
        if my_team == 'radiant' and radiant_win:
            return 'Game Won'
        elif my_team == 'dire' and not radiant_win:
            return 'Game Won'
        else:
            return 'Game Lost'

    def my_kda(self, player_json):
        return player_json['kills'], player_json['deaths'], player_json['assists']

    def my_hero(self, player_json):
        return player_json['hero_id'], player_json['hero_name']

    def my_team(self, player_json):
        if str(player_json['player_slot']) in self.RADIANT_SLOTS:
            return 'radiant'
        elif str(player_json['player_slot']) in self.DIRE_SLOTS:
            return 'dire'
        else:
            raise ValueError

    def my_game_radiant_win(self, match_json):
        return match_json['radiant_win']

    def my_game_duration(self, match_json):
        return match_json['duration']

    def my_game_mode(self, match_json):
        return match_json['game_mode'], match_json['game_mode_name']

    def my_player(self, match_json):
        for player_json in match_json['players']:
            if str(player_json['account_id']) == self.steam_id:
                return player_json

    def retrieve_match_json(self, match_id):
        return self.api.get_match_details(match_id = match_id)

    def retrieve_latest_match_id(self):
        return str(self.api.get_match_history(account_id=self.steam_id)['matches'][0]['match_id'])
