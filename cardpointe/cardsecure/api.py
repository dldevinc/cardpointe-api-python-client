from ..client import Client
from ..credentials import Credentials
from . import resources


class CardSecureAPI:
    def __init__(self, site: str, merchant_id: str, username: str, password: str):
        self._credentials = Credentials(
            site=site,
            merchant_id=merchant_id,
            username=username,
            password=password
        )
        self._client = Client(self._credentials)

        self.tokenize = resources.Tokenize(self._client)
        self.echo = resources.Echo(self._client)
