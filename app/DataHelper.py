import datetime
from concurrent import futures
from typing import Any
from datetime import datetime
import requests
from PyQt5.QtGui import QPixmap


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
    def format_time(unix_time: int) -> Any:
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
    def format_temp(temp: int) -> str:
        """
        This method formats the given value to celsius format
        :param temp: A int value of the temperature.
        :return: A string representation of the temperature with celsius format.
        """
        return str(round(temp)) + "°C"

    @staticmethod
    def format_proc(temp: int) -> str:
        """
        This method formats the value to a percentage format.
        :param temp: A int value to be formatted.
        :return: A string representation of the value with percentage format.
        """
        return str(round(temp)) + "%"

    @staticmethod
    def get_image(url: str):
        """
        This method fetches a single image from url. This method is blocking.
        :param url: A string containing a url.
        :return: A QPixmap object.
        """
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        return None

    @staticmethod
    def get_images(urls: list) -> list:
        """
        This method fetches from the given urls list the images as QPixmap. It is build to be asynchronous.
        :param urls: A list of urls to be fetched.
        :return: A list of QPixmap objects.
        """
        with futures.ThreadPoolExecutor(max_workers=10) as e:
            fs = [
                e.submit(lambda: requests.get(url)) for url in urls
            ]
            results = [
                f.result() for f in fs
            ]

            def build_pixmap(response):
                if response.status_code == 200:
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    return pixmap
            return list(map(lambda x: build_pixmap(x), results))

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
                                   "lon": data["lon"], "city": data["city"] if "city" in data.keys() else None}

            hourly: list = data["hourly"]
            daily: list = data["daily"]

            # Extract data for current representation
            filtered_data["current"]["time"] = FormatDataHelper.format_time(filtered_data["current"]["dt"])
            filtered_data["current"]["humidity"] = FormatDataHelper.format_proc(filtered_data["current"]["humidity"])
            filtered_data["current"]["clouds"] = FormatDataHelper.format_proc(filtered_data["current"]["clouds"])
            filtered_data["current"]["pressure"] = str(filtered_data["current"]["pressure"]) + "hPa"
            filtered_data["current"]["visibility"] = str(filtered_data["current"]["visibility"] / 1000) + "km"
            filtered_data["current"]["wind_speed"] = str(round(filtered_data["current"]["wind_speed"], 1)) + "m/s"
            filtered_data["current"]["feels_like"] = FormatDataHelper.format_temp(
                filtered_data["current"]["feels_like"])
            filtered_data["current"]["weather"][0]["icon"] = "http://openweathermap.org/img/wn/{}.png" \
                .format(filtered_data["current"]["weather"][0]["icon"])
            filtered_data["current"].pop("dt", None)

            # Extract data for hourly representation
            for item in hourly[:10]:
                tmp_time = FormatDataHelper.format_time(item["dt"])
                tmp_icon_uri = "http://openweathermap.org/img/wn/{}.png".format(item["weather"][0]["icon"])
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

            # Extract data for daily representation
            for daily_item in daily[:3]:
                tmp_min_temp = daily_item["temp"]["min"]
                tmp_max_temp = daily_item["temp"]["max"]
                tmp_icon_uri = "http://openweathermap.org/img/wn/{}.png".format(daily_item["weather"][0]["icon"])
                tmp_time = FormatDataHelper.format_time(daily_item["dt"])
                tmp_description = daily_item["weather"][0]["main"]

                daily_item = {
                    "time": tmp_time,
                    "icon": tmp_icon_uri,
                    "min_temp": round(tmp_min_temp),
                    "max_temp": round(tmp_max_temp),
                    "description": tmp_description
                }

                # Append json object to new list
                filtered_data["daily"].append(daily_item)
            return filtered_data
        except Exception as exception:
            print("[FormatDataHelper] - filter_data method error traceback : {}".format(exception))
            return None
