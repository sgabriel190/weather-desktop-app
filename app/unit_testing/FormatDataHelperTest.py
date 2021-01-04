import unittest
import json
from FormatDataHelper import FormatDataHelper


class FormatDataHelperTest(unittest.TestCase):

    # test extract_coord method
    def test_extract_coord(self):
        format_data = FormatDataHelper()
        data = {"coord": {"lon": -0.13, "lat": 51.51}}
        expected_data = {"lon": -0.13, "lat": 51.51}

        result = format_data.extract_coord(data)
        self.assertEqual(result, expected_data)

    # test format_time method
    def test_format_time(self):
        format_data = FormatDataHelper()
        dt = 1609765942
        expected_data = "15:12:22 ~ 04-01-2021"
        result = format_data.format_time(dt)
        self.assertEqual(result, expected_data)

    # test filter_data method
    def test_filter_data(self):
        format_data = FormatDataHelper()
        with open('json2.txt', 'r') as file:
            f = file.read()
        data_given = json.loads(f)
        print(data_given)
        data = format_data.filter_data(data_given)
        self.assertEqual(len(data), 8)
