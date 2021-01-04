import unittest

from RedisConnector import RedisConnector


class RedisConnectorTest(unittest.TestCase):

    # test set data in Redis
    def test_set_data(self):
        database = RedisConnector()
        key = 'test'
        data = {'data': 'test data'}
        exp_resp = database.set_data(key, data)
        self.assertEqual(True, exp_resp)

    # test get data from Redis
    def test_get_data(self):
        database = RedisConnector()
        key = 'test'
        data = database.get_data(key)
        exp_data = {'data': 'test data'}
        self.assertEqual(data, exp_data)

    # test get nonexistent data from Redis
    def test_get_none(self):
        database = RedisConnector()
        key = 'randomkey'
        data = database.get_data(key)
        self.assertEqual(data, None)
