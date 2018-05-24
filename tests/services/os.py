import unittest, subprocess

import magpie.services.os

class TestCoreBot(unittest.TestCase):
    def setUp(self):
        self.hostname = subprocess.check_output(('hostname',)).decode().strip()

    def test_get_uptime(self):
        self.assertIn(self.hostname, magpie.services.os._get_uptime())
        self.assertIn('up', magpie.services.os._get_uptime())

if __name__ == '__main__':
    unnittest.main()
