from http import HTTPStatus, client
import json


class HTTPClient:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.api_url = "api.openweathermap.org"
        self.api_keys = ["6cb9111e5f4a3a33dd47c65cfe06e06e", "b4a3de53f843d2e720c7ed00c6e9dbb2"]
        self.connection = None

    def get(self, url):
        response = None
        try:
            keys = iter(self.api_keys)
            key = next(keys, None)

            while True:
                request_url = f"/data/2.5/{url}&appid={key}"
                self.connection = client.HTTPSConnection(self.api_url, timeout=3)
                self.connection.request('GET', request_url)
                res = self.connection.getresponse()

                response = json.loads(res.read().decode('UTF-8'))
                if "message" in response.keys():
                    if response["message"] == "city not found":
                        response.pop("cod", None)
                        break

                if res.status == HTTPStatus.OK:
                    break

                if res.status != HTTPStatus.UNAUTHORIZED:
                    raise Exception(f"{request_url}, {res.status}, {res.reason}")

                key = next(keys, None)
                if key is None:
                    raise Exception(f"{request_url}, {res.status}, {res.reason}")

        except Exception as exc:
            print(f"[HTTPClient] get error: {exc}")
        finally:
            self.connection.close()
        return response
