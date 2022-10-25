import requests

from .credentials import Credentials
from .exceptions import ApiError


class Client:
    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("auth", (self.credentials.username, self.credentials.password))
        response = requests.request(method, url, **kwargs)

        if 400 <= response.status_code < 500:
            raise ApiError(
                "{} Client Error".format(response.status_code),
                response=response
            )
        elif 500 <= response.status_code < 600:
            raise ApiError(
                "{} Server Error".format(response.status_code),
                response=response
            )

        return response
