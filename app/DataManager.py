from typing import Any

from FormatDataHelper import FormatDataHelper
from HTTPClient import HTTPClient
from RedisConnector import RedisConnector


class DataManager:
    def __init__(self):
        """
            Class constructor, sets up the data manager object.
        """
        self.http_client = HTTPClient()
        self.database = RedisConnector()
        self.format_data = FormatDataHelper()

    def get_current_coords(self, city: str):
        """
             This method gets the coordinates for the searched city. It sends a request to the API
             and filters the response to return only the longitude and latitude

            :param city: A str value of the city.
            :return: The method returns a dict of the coordinates or an error message.
        """
        url = f"weather?q={city}"
        data = self.http_client.get(url)
        return self.format_data.extract_coord(data) if "message" not in data.keys() else data

    def get_info(self, city: str) -> Any:
        """
            This method gets the weather information either by taking it from the database, if exists
            or by making a new request to the API

            :param city: A str value of the city.
            :return: The method returns a dict of the needed data or an error message.
        """
        data_redis = self.database.get_data(city)
        if data_redis is not None:
            print(f"[DataManager] Take data with key='{city}' from database")
            return data_redis

        print(f"[DataManager] New request with key='{city}'")
        data = self.get_current_coords(city)
        if "message" in data.keys():
            if data['message'] == 'city not found':
                print(f"[DataManager] Set data with key '{city}' in database")
                self.database.set_data(key=city, data=data)
                return data

        url = f"onecall?exclude=alerts,minutely&units=metric&lat={data['lat']}&lon={data['lon']}"
        data = self.http_client.get(url)
        data["city"] = city
        data = self.format_data.filter_data(data)
        print(f"[DataManager] Set data with key '{city}' in database")
        self.database.set_data(key=city, data=data)

        return data
