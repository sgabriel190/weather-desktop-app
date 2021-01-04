import json
import unittest

from HTTPClient import HTTPClient


class HTTPClientTest(unittest.TestCase):

    def test_invalid_url(self):
        http_cli = HTTPClient()
        url = "weather?q=Luxemburggg"
        data = http_cli.get(url)
        exp_msg={'message':'city not found'}
        self.assertEqual(data, exp_msg)

