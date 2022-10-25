from typing import ClassVar, Dict
from urllib.parse import urljoin

from .. import utils
from ..client import Client
from ..exceptions import ApiError


class ResourceBase:
    endpoint: ClassVar[str]

    def __init__(self, client: Client):
        self._client = client

    @property
    def site(self):
        return self._client.credentials.site

    @property
    def merchid(self):
        return self._client.credentials.merchant_id

    def get_endpoint(self, path: str = "") -> str:
        """
        Examples:
            "https://httpbin.org/get" + "file" => "https://httpbin.org/get/file"
            "https://httpbin.org/get" + "/file" => "https://httpbin.org/get/file"
            "https://httpbin.org/get/" + "file" => "https://httpbin.org/get/file"
            "https://httpbin.org/get/" + "/file" => "https://httpbin.org/get/file"
        """
        if path and path[0] not in {"?", "#"}:
            # prevent replacement of base URL segments
            endpoint = urljoin(self.endpoint.rstrip("/") + "/", path.lstrip("/"))
        else:
            endpoint = urljoin(self.endpoint, path)

        return endpoint.format(
            site=self.site,
            merchid=self.merchid,
        )


class Tokenize(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardsecure/api/v1/ccn/tokenize"

    def create(
        self,
        *,
        account: str = None,
        devicedata: str = None,
        expiry: str = None,
        cvv: str = None,
        signature: str = None,
        encryptionhandler: str = None,
        unique: str = None,
    ) -> Dict:
        """
        A request to the tokenize endpoint returns a CardSecure token generated
        from the data provided in the request.

        A tokenize request includes payment account data in either the `account`
        or `devicedata` field.

        Use the `account` field to provide a clear or encrypted payment account
        number (PAN) or ACH account number (in the format <routing>/<account>).

        If the `account` data is encrypted, include the encryptionhandler parameter
        to instruct CardSecure to decrypt the data using the private key for your site.

        Use the `devicedata` field to provide track data received from a terminal device
        for an MSR (swipe), EMV (chip), or NFC (contactless) transaction, or a digital
        wallet payload (for example for a Google Pay transaction).

        The tokenize response includes a token generated from the account data.
        You can then use this token to submit an authorization request
        to the CardPointe Gateway.

        :param account:
            One of the following:
                1) A clear or encrypted payment account number (PAN);
                2) An ACH routing and account number string in the format
                   `<routing>/<account>` for eCheck transactions.
            If `encryptionhandler` is provided, the account is treated
            as an encrypted PAN.
        :param devicedata:
            One of the following:
                1) Encrypted track data retrieved using a card reader
                   or terminal device (MSR/EMV/NFC);
                2) Apple Pay payment token data (see the Apple Pay Developer
                   Guide for detailed information);
                3) Google Pay wallet payload (see the Google Pay Developer
                   Guide for detailed information).
        :param expiry:
            Optional, the card expiration date in one of the following formats
            MMYY, YYYYM (for single-digit months), YYYYMM, YYYYMMDD.
        :param cvv:
            Optional, the 3 or 4 digits card verification value (CVV).
            Must be a 3 or 4 character numeric string; strings greater than 4 characters
            or fewer than 3 characters are not supported.
        :param signature:
            JSON escaped, Base64 encoded, Gzipped, BMP of signature data.
        :param encryptionhandler:
            One of the following :
                1) For an encrypted PAN or ACH, specify `RSA`;
                2) For an Apple Pay payment token, specify `EC_APPLE_PAY`;
                3) For a Google Pay wallet payload, specify `EC_GOOGLE_PAY`.
        :param unique:
            Specifies whether or not a unique token should be generated.
            Specify `true` to generate a unique token.
            Defaults to `false`.

        :raises RuntimeError:
            if neither `account` nor `devicedata` is defined.
        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.cardsecure.api import CardSecureAPI

            api = CardSecureAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            api.tokenize.create(
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv="123"
            )
        """
        if account is None and devicedata is None:
            raise RuntimeError("Either account or devicedata are required.")

        data = utils.clean_data({
            "account": account,
            "devicedata": devicedata,

            "expiry": expiry,
            "cvv": cvv,
            "signature": signature,
            "encryptionhandler": encryptionhandler,
            "unique": unique,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["errorcode"] != 0:
            raise ApiError(result["message"], response=response)

        return result

    def update(
        self,
        *,
        account: str,
        expiry: str = None,
        cvv: str = None,
    ) -> Dict:
        """
        The CardSecure API supports the ability to update a payment card token to include
        the CVV and expiration date associated with the card.

        Note: If you use a card reader or terminal to capture track data,
        you SHOULD NOT use this method. Updating the token may delete the track data,
        making the token unusable.

        :param account:
            A token representing a payment account number.
        :param expiry:
            Optional, the card expiration date in one of the following formats
            MMYY, YYYYM (for single-digit months), YYYYMM, YYYYMMDD.
        :param cvv:
            Optional, the 3 or 4 digits card verification value (CVV).
            Must be a 3 or 4 character numeric string; strings greater than 4 characters
            or fewer than 3 characters are not supported.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.cardsecure.api import CardSecureAPI

            api = CardSecureAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            api.tokenize.update(
                account="9418594164541111",
                expiry="1222",
                cvv="123"
            )
        """
        data = utils.clean_data({
            "account": account,
            "expiry": expiry,
            "cvv": cvv,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["errorcode"] != 0:
            raise ApiError(result["message"], response=response)

        return result


class Echo(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardsecure/api/v1/echo"

    def create(
        self,
        *,
        message: str = None,
    ) -> Dict:
        """
        A call to the echo service endpoint sends a ping command to the CardSecure
        server to verify the application's connection. You can include a message
        in the request, which is returned in the response if the request is successful.
        If the request fails, an error message is returned with a corresponding error code.

        :param message:
            A message to send in the ping request and receive in the response. The value
            can be blank, however the message field must be included in the request.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.cardsecure.api import CardSecureAPI

            api = CardSecureAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            api.echo.create(
                message="Hello",
            )
        """
        data = utils.clean_data({
            "message": message,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["errorcode"] != 0:
            raise ApiError(result["message"], response=response)

        return result
