import unittest

from HTTPClient import HTTPClient


class HTTPClientTest(unittest.TestCase):

    # test query with invalid city
    def test_invalid_city(self):
        http_cli = HTTPClient()
        url = "weather?q=Luxemburggg"
        data = http_cli.get(url)
        exp_msg = {'message': 'city not found'}
        self.assertEqual(data, exp_msg)

    # test query with invalid coordinates
    def test_invalid_coordinates(self):
        http_cli = HTTPClient()
        lat = 1000
        lon = 0
        url = f"onecall?exclude=alerts,minutely&units=metric&lat={lat}&lon={lon}"
        data = http_cli.get(url)
        exp_msg = {'cod': '400', 'message': 'wrong latitude'}
        self.assertEqual(data, exp_msg)

    # test invalid path to API
    def test_invalid_request(self):
        http_cli = HTTPClient()
        url = "weathher?q=Luxemburg"
        data = http_cli.get(url)
        exp_msg = {'cod': '404', 'message': 'Internal error'}
        self.assertEqual(data, exp_msg)
