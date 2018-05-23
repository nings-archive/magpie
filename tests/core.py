import configparser, unittest

import magpie.core

config = configparser.ConfigParser()
config.read('config.ini')

class TestCoreBot(unittest.TestCase):
    def setUp(self):
        self.bot = magpie.core.Bot(
            token=config['telegram']['token'],
            admin_id=config['telegram']['admin_id'])

    def test_auth(self):
        self.assertIsNotNone(self.bot.get_me())

if __name__ == '__main__':
    unnittest.main()
