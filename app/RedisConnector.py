import abc
import datetime
import json
from typing import Any

from redis import Redis


class RedisConnector(metaclass=abc.ABCMeta):

    def __init__(self, host: str = 'localhost', port: int = 6379, password: str = None):
        """
            The only class constructor of the RedisConnector.
            This constructor allows the class to be created with the default parameters or
            other parameters if the redis server runs on other settings.

            :param host: A string representing the hostname of the redis server.
            :param port: A int value for the port number of the redis server.
            :param password: A string value for the password of the redis server.
        """
        super().__init__()
        self.__HOST: str = host
        self.__PORT: int = port
        self.__password: str = password
        self.__redis_client: Redis = Redis(
            host=self.__HOST,
            port=self.__PORT,
            password=self.__password,
            db=0,
            socket_timeout=None
        )

    def set_data(self, key: str, data: dict, expire: bool = True) -> bool:
        """
            This method adds a new key:value pair to the redis server. The pair is set automatically to expire on the hour.
            E.g.: data is set on 14:34 and it will expire on 15:00.

            :param key: A str value of the key to be inserted.
            :param data: A dict of the data to be inserted.
            :param expire: A bool value which sets whether the pair will expire or not.
            :return: The method returns True if the insert operation was successful or False otherwise.
        """
        try:
            delta = datetime.timedelta(hours=1)
            now = datetime.datetime.now()
            next_hour = (now + delta).replace(microsecond=0, second=0, minute=2)
            wait_seconds = (next_hour - now).seconds

            self.__redis_client.set(key, json.dumps(data), ex=None if expire is False else wait_seconds)
            return True
        except Exception as exception:
            print("[RedisConnector] - set_data method error traceback: {}".format(exception))
            return False

    def get_data(self, key: str) -> Any:
        """
            This method searches into the redis server for the key:value pair by its key and returns the value.
            The value will be returned as a python dictionary(json).

            :param key: The key to be searched in the redis server.
            :return: The value of the key searched if it exists or None if it does not exist or if any exception
             occurred.
        """
        try:
            data: bytearray = self.__redis_client.get(key)
            return json.loads(data.decode('utf-8')) if data is not None else data
        except Exception as exception:
            print("[RedisConnector] - get_data method error traceback: {}".format(exception))
            return None
