import datetime
import json
from typing import Any
from datetime import datetime


class FormatDataHelper:

    @staticmethod
    def extract_coord(data: dict) -> Any:
        """
        This method extracts the coordinates of the city the client is searching information about.
        :param data: A dict of the data to be filtered.
        :return: The method returns a dict of the longitude and latitude
        """
        try:
            coordinates = data["coord"]
            return coordinates
        except Exception as exception:
            print("[FormatDataHelper] - extract_coord method error traceback : {}".format(exception))
            return None

    @staticmethod
    def format_time(unix_time: int) -> str:
        """
        This method converts the unix timestamp into a readable date.
        :param unix_time: The number of seconds that have elapsed since the Unix epoch
        :return: The method returns a string of the current date
        """
        try:
            time = datetime.fromtimestamp(unix_time).strftime('%H:%M:%S ~ %d-%m-%Y')
            return time
        except Exception as exception:
            print("[FormatDataHelper] - format_time method error traceback : {}".format(exception))
            return None

    @staticmethod
    def filter_data(data: dict) -> Any:
        """
        This method extracts from the main dictionary the main data used in the app.
        :param data: A dict of the data to be filtered.
        :return: The method returns a dict of the relevant data.
        """
        try:
            filtered_data: dict = {"timezone": data["timezone"], "timezone_offset": data["timezone_offset"],
                                   "current": data["current"], "daily": [], "hourly": [], "lat": data["lat"],
                                   "lon": data["lon"]}

            hourly: list = data["hourly"]
            daily: list = data["daily"]

            for item in hourly[:10]:
                tmp_time = FormatDataHelper.format_time(item["dt"])
                tmp_icon_uri = "/img/wn/{}.png".format(item["weather"][0]["icon"])
                tmp_temperature = item["temp"]
                tmp_description = item["weather"][0]["main"]

                item = {
                    "time": tmp_time,
                    "icon": tmp_icon_uri,
                    "temperature": round(tmp_temperature),
                    "description": tmp_description
                }

                # Append json object to new list
                filtered_data["hourly"].append(item)

            for daily_item in daily[:3]:
                tmp_min_temp = daily_item["temp"]["min"]
                tmp_max_temp = daily_item["temp"]["max"]
                tmp_icon_uri = "/img/wn/{}.png".format(daily_item["weather"][0]["icon"])
                tmp_time = FormatDataHelper.format_time(daily_item["dt"])
                tmp_description = daily_item["weather"][0]["main"]

                daily_item = {
                    "time": tmp_time,
                    "icon": tmp_icon_uri,
                    "min_temp": round(tmp_min_temp),
                    "max_temp": round(tmp_max_temp),
                    "description":tmp_description
                }

                # Append json object to new list
                filtered_data["daily"].append(daily_item)
            return filtered_data
        except Exception as exception:
            print("[FormatDataHelper] - filter_data method error traceback : {}".format(exception))
            return None
