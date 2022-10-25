from ..client import Client
from ..credentials import Credentials
from . import resources


class GatewayAPI:
    def __init__(self, site: str, merchant_id: str, username: str, password: str):
        self._credentials = Credentials(
            site=site,
            merchant_id=merchant_id,
            username=username,
            password=password
        )
        self._client = Client(self._credentials)

        self.inquireMerchant = resources.InquireMerchant(self._client)
        self.authorization = resources.Authorization(self._client)
        self.capture = resources.Capture(self._client)
        self.inquire = resources.Inquire(self._client)
        self.inquireByOrderId = resources.InquireByOrderId(self._client)
        self.void = resources.Void(self._client)
        self.voidByOrderId = resources.VoidByOrderId(self._client)
        self.refund = resources.Refund(self._client)
        self.profile = resources.Profile(self._client)
        self.signature = resources.Signature(self._client)
        self.bin = resources.BIN(self._client)
        self.funding = resources.Funding(self._client)
