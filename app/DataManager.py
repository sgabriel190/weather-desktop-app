from HTTPClient import HTTPClient
from RedisConnector import RedisConnector


class DataManager:
    def __init__(self):
        self.http_client = HTTPClient()
        self.database = RedisConnector()

    def get_current_coords(self, city):
        url = f"weather?q={city}"
        data = self.http_client.get(url)
        # extract_coords(..)
        return data

    def get_info(self, coords):
        city = "London"
        data = self.database.get_data(city)

        if data is None:
            print(f"[DataManager] New request with key='{city}'")
            url = f"onecall?exclude=alerts,minutely&units=metric&lat={coords['lat']}&lon={coords['lon']}"
            data = self.http_client.get(url)
            # filter_data(..)

            print(f"[DataManager] Set data with key {city} in database")
            self.database.set_data(key=city, data=data)
        else:
            print(f"[DataManager] Take data with key='{city}' from database")

        return data
