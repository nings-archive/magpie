import os, json
import telegram

class Core:
    '''
    Core handles all interactions with python-telegram-bot, and the system.
    Other modules will inherit from this class.
    '''
    PATH_TO_CONFIG = os.path.expanduser('~/.magpie/config.json')

    def __init__(self):
        self.config = Core.load_config()
        self.bot_token = self.config['core']['token']
        self.chat_id   = self.config['core']['chat_id']
        self.dl_dir    = self.config['core']['dl_dir']
        self.bot = telegram.Bot(token=self.bot_token)

    def send_me(self, text):
        return self.bot.send_message(
            chat_id=self.chat_id,
            parse_mode=telegram.ParseMode.HTML,
            text=text
        )

    def send_document(self, document_path):
        return self.bot.send_document(
            chat_id=self.chat_id,
            document=open(document_path, 'rb')
        )

    def is_my_chat_id(self, this_chat_id):
        if str(this_chat_id) == str(self.chat_id):
            return True
        else:
            return False

    @classmethod
    def load_config(cls):
        with open(cls.PATH_TO_CONFIG, 'r') as file:
            return json.loads(file.read())

    @classmethod
    def save_config(cls, config):
        with open(cls.PATH_TO_CONFIG, 'w') as file:
            json.dump(config, file, indent=4)

