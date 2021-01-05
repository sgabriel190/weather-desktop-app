import unittest
import json

from DataManager import DataManager


class DataManagerTest(unittest.TestCase):

    # test returned dict of coordinates for valid city
    def test_coords_valid_city(self):
        data_manager = DataManager()
        coords = data_manager.get_current_coords('Dublin')
        exp_coords = {'lon': -121.9358, 'lat': 37.7021}
        self.assertEqual(coords, exp_coords)

    # test returned message for invalid city
    def test_coords_invalid_city(self):
        data_manager = DataManager()
        coords = data_manager.get_current_coords('Dublinn')
        with open('city_not_found.txt', 'r') as file:
            exp_msg = json.loads(file.read())
        self.assertEqual(coords, exp_msg)

    # test the dictionary returned has the right amount of information
    def test_filtered_data(self):
        data_manager = DataManager()
        city = data_manager.get_info("Amsterdam")
        with open('amsterdam.txt', 'r') as file:
            f = file.read()
        city_expected = json.loads(f)
        self.assertEqual(len(city), len(city_expected))

    # test the city returned is the right city
    def test_city(self):
        data_manager = DataManager()
        city = data_manager.get_info("Amsterdam")
        with open('amsterdam.txt', 'r') as file:
            f = file.read()
        city_expected = json.loads(f)
        self.assertEqual(city["city"], city_expected["city"])

    # test message for non-existent city
    def test_city_not_found(self):
        data_manager = DataManager()
        with self.assertRaises(Exception):
            city = data_manager.get_info("vazlui")
