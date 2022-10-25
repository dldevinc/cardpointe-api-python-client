from decimal import Decimal
from typing import ClassVar, Dict, List, Union
from urllib.parse import urljoin

from .. import utils
from ..client import Client
from ..exceptions import ApiError
from .constants import ResponseStatus


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


class InquireMerchant(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/inquireMerchant/{merchid}"

    def get(self) -> Dict:
        """
        Returns information on the merchant account configuration.

        This can be helpful for partners who need to validate their
        CardPointe merchant IDs or for businesses with merchants operating
        in multiple locations, to ensure that the merchant ID is boarded
        to the correct site.

        :raises ApiError:
            if response's status code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            api.inquireMerchant.get()
        """
        endpoint = self.get_endpoint()
        response = self._client.request("GET", endpoint)
        return response.json()


class Authorization(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/auth"

    def create(
        self,
        *,
        amount: Union[str, Decimal],
        account: str = None,
        expiry: str = None,
        cvv2: str = None,
        capture: str = None,
        currency: str = None,
        userfields: Dict = None,

        name: str = None,
        company: str = None,
        address: str = None,
        address2: str = None,
        city: str = None,
        region: str = None,
        country: str = None,
        postal: str = None,
        phone: str = None,
        email: str = None,

        profile: str = None,
        cof: str = None,
        cofpermission: str = None,
        cofscheduled: str = None,

        bankaba: str = None,
        ecomind: str = None,
        orderid: str = None,
        receipt: str = None,
        tokenize: str = None,
        signature: str = None,
        track: str = None,
        bin: str = None,
        auoptout: str = None,
        authcode: str = None,
        taxexempt: str = None,
        taxamnt: Union[str, Decimal] = None,
        termid: str = None,
        accttype: str = None,
    ) -> Dict:
        """
        Authorization is the initial step in accepting payment from a cardholder.
        This action "authorizes" or requests permission from the bank to transfer
        money from the cardholder to the merchant.

        :param amount:
            Amount with decimal or without decimal in currency minor units
            (for example, USD Pennies or EUR Cents).
            The value can be a positive or negative amount or 0,
            and is used to identify the type of authorization, as follows:
            1) Positive - Authorization request.
            2) Zero - Account Verification request.
            3) Negative - Refund without reference (Forced Credit).
            Merchants must be configured to process forced credit transactions.
            To refund an existing authorization, use Refund.
        :param account:
            Can be:
                1) CardSecure Token - a token representing a payment account number.
                2) Clear text card number.
                3) Bank Account Number. When using BAN, the `bankaba` field is also required.
            Note: To use a stored profile, omit the `account` property and supply
            the profile ID in the `profile` field instead.
        :param expiry:
            Card expiration in one of the following formats
            MMYY, YYYYM (for single-digit months), YYYYMM, YYYYMMDD.
            Not required for eCheck (ACH) or digital wallet (for example, Apple Pay
            or Google Pay) payments.
        :param cvv2:
            The 3 or 4-digit cardholder verification value (CVV2/CVC/CID) present
            on the card.
        :param capture:
            Optional, specify Y to capture the transaction for settlement if approved.
            Defaults to N if not provided.
        :param currency:
            Currency of the authorization (for example, USD for US dollars or CAD
            for Canadian Dollars).
            Note: If specified in the auth request, the currency value must match
            the currency that the MID is configured for. Specifying the incorrect
            currency will result in a "Wrong currency for merch" response.
        :param userfields:
            The value of the userfields object is a series of name-value pairs
            that are meaningful to the merchant. The name and value fields can
            include any string value, and you can include as many fields as necessary.

        :param name:
            Account holder's name, optional for credit cards and electronic checks (ACH).
        :param company:
            Account holder's company name.
        :param address:
            Account holder's street address, required for AVS verification.
        :param address2:
            Second address line (for example, apartment or suite number) if applicable.
        :param city:
            Account holder's city.
        :param region:
            Account holder's region, US State, Mexican State, Canadian Province.
        :param country:
            Account holder's country (2-character country code), defaults to "US".
            Required for all non-US addresses.
        :param postal:
            The account holder's postal code. If country is "US", must be 5 or 9 digits.
            Otherwise any alphanumeric string is accepted. Defaults to "55555"
            if not included in the request or stored profile.
        :param phone:
            Account holder's phone number. Optional for credit cards, but required
            for E-check/ACH authorizations.
        :param email:
            Account holder's email address.

        :param profile:
            Optional, to create a stored customer profile or to use an existing profile.
            To create a profile using the account holder data provided in the request,
            specify Y.
            To use an existing profile for this authorization, omit the account parameter
            and instead use the profile parameter to supply the 20-digit profile id
            and 1-3-digit account id string in the format `<profileid>/<acctid>`.
            Note: If the authorization request fails or is declined, the profile
            is not created.
            Note: You can submit a $0 authorization, including CVV and AVS verification,
            to validate the customer's information before creating a profile.
        :param cof:
            Required for initial and subsequent transactions using stored cardholder
            payment information. The `cof` parameter specifies whether the transaction
            is initiated by the customer or merchant.
            Specify one of the following values:
                C - Customer-Initiated Transaction (CIT);
                M - Merchant-Initiated Transaction (MIT).
        :param cofpermission:
            Optionally, when `"profile":"y"` to create a stored profile, include
            `"cofpermission":"y"` to indicate that you obtained the cardholder's
            permission to store their payment data. This field is only used
            for reporting purposes, via the get profile response.
            Specify one of the following values:
                Y - The cardholder provided their consent to store and reuse their
                    payment details;
                N - The cardholder did not provide their consent.
            Defaults to N if not provided.
        :param cofscheduled:
            Required for transactions using stored cardholder payment information.
            For a merchant-initiated transaction (MIT), the `cofscheduled` parameter
            specifies whether the transaction is a one-time payment or a scheduled
            recurring payment.
            Specify one of the following values:
                Y - The transaction is a scheduled (automated) payment;
                N - The transaction is a one-time payment.

        :param bankaba:
            Bank routing (ABA) number. Required for eCheck (ACH) authorizations
            when a bank account number is provided in the `account` field.
            `bankaba` is not required if a CardSecure token (generated
            from the account/bankaba pair) is provided in the `account` field.
        :param ecomind:
            A transaction origin indicator, for card-not-present and eCheck (ACH)
            transactions only. For card-not-present transactions, one of the following
            values:
                T - telephone or mail payment;
                R - recurring billing;
                E - e-commerce web or mobile application.
            Note: You should include the appropriate `ecomind` value for all
            card-not-present transactions, to ensure that the transaction processes
            at the appropriate interchange level. Do not include `ecomind` for card-present
            transactions, in which the payment card data is obtained using a POS device.
        :param orderid:
            Source system order number.
            Note: If you include an order ID it must meet the following requirements:
            1) The order ID must be a unique value. Using duplicate order IDs can lead
               to the wrong transaction being voided in the event of a timeout.
            2) The order ID must not include any portion of a payment account number (PAN),
               and no portion of the order ID should be mistaken for a PAN. If the order
               ID passes the Luhn check performed by the CardPointe Gateway, the value
               will be masked in the database, and attempts to use the order ID
               in an inquire, void, or refund request will fail.
        :param receipt:
            Optional, to return receipt data fields in the authorization response
            to print on a receipt.
            Specify one of the following values:
                Y - return the `receipt` data;
                json - to return the `receiptObj` data.
            Defaults to N if not provided.
        :param tokenize:
            Optional, specify N or omit to return an account token in the account field
            in the response. If tokenize is Y the masked card or ACH account number
            is returned in the response.
        :param signature:
            JSON escaped, Base64 encoded, Gzipped, BMP of signature data.
            If the authorization is using a token with associated signature data,
            then the signature from the token is used.
        :param track:
            Payment card track data captured using a supported card reader device
            (for example, a desktop card reader device). Can be unencrypted
            Track 1 or Track 2 data, or encrypted swipe data (containing Track 1
            and/or Track 2) data.
        :param bin:
            Optional, to return BIN lookup fields in the authorization response.
            Specify Y to retrieve the BIN data for the card.
            Defaults to N if not provided.
        :param auoptout:
            Optional, when creating a profile, to specify whether or not the profile
            is set to opt out of the Card Account Updater service. Requires the merchant
            account to be enrolled in the Card Account Updater add-on.
            Specify one of the following values:
                Y - updates are not retrieved for this profile;
                N - updates are retrieved for this profile.
            Defaults to N if not provided.
        :param authcode:
            Authorization code from original authorization (VoiceAuth).
            For Voice/Capture-Only, include valid `authcode`.
        :param taxexempt:
            If `taxexempt` is set to N for the transaction and a tax is not passed,
            the default configuration data is used. If `taxexempt` is set to Y,
            the `taxamnt` is $0.00.
        :param taxamnt:
            Tax amount for the order, either decimal or in currency minor units
            (for example, USD Pennies or MXN Centavos).
            If `taxexempt` is Y, `taxamnt` must be zero or omitted. If `taxexempt` is N,
            `taxamnt` must be a positive, non-zero value.
        :param termid:
            The Terminal Device ID, required when the Send Terminal ID for Reporting
            feature is enabled for First Data ClientLine Reporting.
            `termid` must be exactly 8 characters long, and the last 5 characters
            (used to display on the report) must be numbers.
            Note: This field is not used for CardPointe transaction reporting.
        :param accttype:
            The account type, not required unless one of the following:
                ECHK - Electronic checking account, for ACH transactions;
                ESAV - Electronic savings account, for ACH transactions;
                PDEBIT - For PINless Debit transactions. Must be enabled for the
                         merchant account.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                name="John Snow",
                address="Green street 16",
                city="Denver",
                region="CO",
                postal="80014",
                phone="12345678900",
                email="user@gmail.com",
                ecomind="E",
                userfields={
                    "invoice_id": "456",
                    "user_id": "123",
                }
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "amount": str(amount),
            "account": account,
            "expiry": expiry,
            "cvv2": cvv2,
            "capture": capture,
            "currency": currency,
            "userfields": userfields,

            "name": name,
            "company": company,
            "address": address,
            "address2": address2,
            "city": city,
            "region": region,
            "country": country,
            "postal": postal,
            "phone": phone,
            "email": email,

            "profile": profile,
            "cof": cof,
            "cofpermission": cofpermission,
            "cofscheduled": cofscheduled,

            "bankaba": bankaba,
            "ecomind": ecomind,
            "orderid": orderid,
            "receipt": receipt,
            "tokenize": tokenize,
            "signature": signature,
            "track": track,
            "bin": bin,
            "auoptout": auoptout,
            "authcode": authcode,
            "taxexempt": taxexempt,
            "taxamnt": str(taxamnt) if taxamnt is not None else None,
            "termid": termid,
            "accttype": accttype,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class Capture(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/capture"

    def create(
        self,
        *,
        retref: str,
        amount: Union[str, Decimal] = None,
        receipt: str = None,
        authcode: str = None,
    ) -> Dict:
        """
        The capture service queues the transaction amount for settlement.
        Capture can occur within the authorization request or subsequently.

        :param retref:
            CardPointe retrieval reference number from authorization response.
        :param amount:
            Capture amount in decimal or in currency minor units (for example,
            USD Pennies or MXN Centavos).
            When the amount is omitted, the original authorization amount is captured.
            If the amount to be captured is more than the authorized amount
            (such as a tip adjustment), ensure that the merchant is appropriately
            entitled with this capability.
        :param receipt:
            Optional, to return receipt data fields in the response.
            Specify Y to return additional merchant and transaction data to print
            on a receipt.
            Defaults to N if not provided.
        :param authcode:
            Authorization code from original authorization request.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Authorize
            auth_data = api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                postal="80014",
                ecomind="E"
            )

            # Capture
            api.capture.create(
                retref=auth_data["retref"]
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "retref": retref,
            "authcode": authcode,
            "amount": str(amount) if amount is not None else None,
            "receipt": receipt,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class Inquire(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/inquire"

    def get(
        self,
        *,
        retref: str,
    ) -> Dict:
        """
        The inquire service returns information for an individual transaction,
        including its settlement status (`setlstat`) and the response codes
        from the initial authorization.

        :param retref:
            The retrieval reference number from the original authorization response.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Inquire
            api.inquire.get(
                retref="296562170203"
            )
        """
        endpoint = self.get_endpoint("{}/{{merchid}}".format(retref))
        response = self._client.request("GET", endpoint)
        result = response.json()

        # do not raise an exception for declined transactions
        if "account" not in result and result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class InquireByOrderId(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/inquireByOrderid"

    def get(
        self,
        *,
        orderid: str,
        set_: str = None,
    ) -> Union[Dict, List[Dict]]:
        """
        Similarly to the inquire endpoint, requests to the inquireByOrderid endpoint
        return information for an authorization; however, inquireByOrderid references
        the Order ID associated with the transaction instead of the retrieval reference
        number (retref).

        This allows you to get information about a transaction if the original
        authorization was interrupted and no response was returned, including
        the retref (if one was generated).

        It is strongly recommended that you use a unique order ID for every transaction,
        if you are using order IDs. Doing so allows you to more easily and accurately
        retrieve data on all transactions.

        :param orderid:
            The order ID from the original authorization response.
        :param set_:
            Set to "1" to restrict the inquiry to the merchant ID (MID) specified
            in the request. If you have multiple MIDs and want to search for the order ID
            across all MIDs, omit this parameter.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Authorize
            auth_data = api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                postal="80014",
                ecomind="E",
                orderid="773"
            )

            # Inquire by Order ID
            api.inquireByOrderId.get(
                orderid="773"
            )
        """
        path = "{}/{{merchid}}".format(orderid)
        if set_:
            path += "/{}".format(set_)

        endpoint = self.get_endpoint(path)
        response = self._client.request("GET", endpoint)
        result = response.json()

        if isinstance(result, dict):
            # do not raise an exception for declined transactions
            if "account" not in result and result["respstat"] != ResponseStatus.APPROVED:
                raise ApiError(result["resptext"], response=response)

        return result


class Void(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/void"

    def create(
        self,
        *,
        retref: str,
        amount: Union[str, Decimal] = None,
    ) -> Dict:
        """
        The void service cancels a transaction that is in either "Authorized"
        or "Queued for Capture" status.

        Note: Partial voids are not supported for debit transactions.
        If you specify a partial void amount for a debit transaction, the entire amount
        is voided. Omit the amount or specify the full amount for a debit void.

        :param retref:
            The retrieval reference number from the original authorization response.
        :param amount:
            Optional. If omitted or equal to $0, the full amount is voided.
            If no capture has taken place (`setlstat`:`Authorized`), you can specify
            a partial amount to void to reduce the amount of the authorization.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Authorize
            auth_data = api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                postal="80014",
                ecomind="E"
            )

            # Void
            api.void.create(
                retref=auth_data["retref"]
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "retref": retref,
            "amount": str(amount) if amount is not None else None,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class VoidByOrderId(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/voidByOrderId"

    def create(
        self,
        *,
        orderid: str,
        amount: Union[str, Decimal] = None,
    ) -> Dict:
        """
        The voidByOrderId endpoint is used to look up and void a transaction record
        using the order ID supplied in the original authorization request.
        If the order ID supplied in a voidByOrderId request matches a transaction record
        for the specified merchant, the authorization is voided and a response is returned.

        Note: Partial voids are not supported for debit transactions.
        If you specify a partial void amount for a debit transaction, the entire amount
        is voided. Omit the amount or specify the full amount for a debit void.

        :param orderid:
            The order Id from the original authorization response.
        :param amount:
            Optional. If omitted or equal to $0, the full amount is voided.
            If no capture has taken place (`setlstat`:`Authorized`), you can specify
            a partial amount to void to reduce the amount of the authorization.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Authorize
            auth_data = api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                postal="80014",
                ecomind="E",
                orderid="773"
            )

            # Void by Order Id
            api.voidByOrderId.create(
                orderid="773"
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "orderid": orderid,
            "amount": str(amount) if amount is not None else None,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class Refund(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/refund"

    def create(
        self,
        *,
        retref: str,
        amount: Union[str, Decimal] = None,
        orderid: str = None,
    ) -> Dict:
        """
        The refund service is used for transactions that are in a settled status.

        If you do not have a retref for the transaction, you can return funds
        to an account by passing a negative amount (forced credit) in an authorization
        and subsequent capture request.

        :param retref:
            The retrieval reference number from the original authorization.
        :param amount:
            Positive amount with decimal or amount without decimal in currency minor
            units (for example, USD Pennies or MXN Centavos) for partial refunds.
            If no value is provided, the full amount of the transaction is refunded.
        :param orderid:
            Optional, a unique order number for the refund transaction, to specify
            a unique identifier for the refund instead of retaining the order ID
            from the original authorization (if present).
            If an `orderid` is present in the refund request, it will be stored
            and associated with the refund transaction record.
            If an `orderid` is not present in the refund request, the refund will
            be associated with the `orderid` from the original authorization,
            if one was provided.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Authorize & Capture
            auth_data = api.authorization.create(
                amount="0.50",
                account="4111 1111 1111 1111",
                expiry="1222",
                cvv2="123",
                capture="Y",
                postal="80014",
                ecomind="E"
            )

            # Refund
            api.refund.create(
                retref=auth_data["retref"]
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "retref": retref,
            "amount": str(amount) if amount is not None else None,
            "orderid": orderid
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class Profile(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/profile"

    def get(
        self,
        *,
        profile: str,
    ) -> Union[Dict, List[Dict]]:
        """
        A GET request to the profile endpoint returns the stored data for the specified
        profile ID.

        If the profile includes more than one account, you can specify an account ID
        to retrieve data for a specific account. If you do not include an account ID,
        then data for all accounts in the profile is returned in the response.

        :param profile:
            20-digit profile ID and (optional) 3-digit account ID string in the format
            <profile id>/<account id>.
            If the account ID is omitted, then all accounts in the profile are returned.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Get profile
            api.profile.get(
                profile="14859162937614814455/1"
            )
        """
        if "/" in profile:
            profile_id, account_id = profile.split("/")
        else:
            profile_id, account_id = profile, ""

        endpoint = self.get_endpoint("{}/{}/{{merchid}}".format(
            profile_id,
            account_id
        ))
        response = self._client.request("GET", endpoint)
        result = response.json()

        if isinstance(result, list) and len(result) == 1:
            result = result[0]

        if "respstat" in result and result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result

    def create(
        self,
        *,
        account: str,
        expiry: str,
        defaultacct: str = None,

        name: str = None,
        company: str = None,
        address: str = None,
        address2: str = None,
        city: str = None,
        region: str = None,
        country: str = None,
        postal: str = None,
        phone: str = None,
        email: str = None,

        profile_id: str = None,
        cofpermission: str = None,

        bankaba: str = None,
        auoptout: str = None,
        accttype: str = None,
    ) -> Dict:
        """
        A POST call to the profile endpoint creates a new profile or adds a new account
        to an existing profile.

        The service tokenizes the account property and creates the profile with a token
        and profile ID and optional account ID. If the profile includes multiple accounts,
        one account ID in the profile can be marked as the default account by setting
        the `defaultacct` parameter to "Y." The default account will be used for
        all authorization requests when only the profile ID is supplied.

        You can submit a $0 authorization, including CVV and AVS verification,
        to validate the customer's information before creating a profile.

        :param account:
            Can be:
                1) CardSecure Token - a token representing a payment account number.
                2) Clear text card number.
                3) Bank Account Number. When using BAN, the `bankaba` field is also required.
            Note: To use a stored profile, omit the account property and supply
            the profile ID in the profile field instead.
        :param expiry:
            Card expiration in one of the following formats
            MMYY, YYYYM (for single-digit months), YYYYMM, YYYYMMDD.
            Not required for eCheck (ACH) or digital wallet (for example, Apple Pay
            or Google Pay) payments.
        :param defaultacct:
            "Y" to assign as default account.

        :param name:
            Account holder's name, optional for credit cards and electronic checks (ACH).
        :param company:
            Account holder's company name.
        :param address:
            Account holder's street address, required for AVS verification.
        :param address2:
            Second address line (for example, apartment or suite number) if applicable.
        :param city:
            Account holder's city.
        :param region:
            Account holder's region, US State, Mexican State, Canadian Province.
        :param country:
            Account holder's country (2-character country code), defaults to "US".
            Required for all non-US addresses.
        :param postal:
            The account holder's postal code. If country is "US", must be 5 or 9 digits.
            Otherwise any alphanumeric string is accepted. Defaults to "55555"
            if not included in the request or stored profile.
        :param phone:
            Account holder's phone number. Optional for credit cards, but required
            for E-check/ACH authorizations.
        :param email:
            Account holder's email address.

        :param profile_id:
            To add an account to an existing profile, include an existing profile ID.
        :param cofpermission:
            Optionally specifies whether or not the cardholder provided consent
            to store their payment details in a profile.
            Specify one of the following values:
                Y - The cardholder provided their consent to store and reuse their
                    payment details;
                N - The cardholder did not provide their consent.
            Defaults to N if not provided.

        :param bankaba:
            Bank routing (ABA) number. Required for eCheck (ACH) authorizations
            when a bank account number is provided in the account field.
            `bankaba` is not required if a CardSecure token (generated
            from the account/bankaba pair) is provided in the account field.
        :param auoptout:
            Specifies whether or not the profile is set to opt out of the CardPointe
            Account Updater service. Requires the merchant account to be enrolled
            in the Card Account Updater add-on.
            Specify one of the following values:
                Y - updates are not retrieved for this profile;
                N - updates are retrieved for this profile.
            Defaults to N if not provided.
        :param accttype:
            One of PPAL, PAID, GIFT, PDEBIT, otherwise not required.

        :raises ValueError: if an account ID is set in `profile_id`.
        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Create new profile
            profile_data = api.profile.create(
                account="4111 1111 1111 1111",
                expiry="1222",
                defaultacct="Y",
                name="John Snow",
                address="Green street 16",
                city="Denver",
                region="CO",
                postal="80014",
                phone="12345678900",
                email="user@gmail.com"
            )

            # Add another account to an existing profile
            api.profile.create(
                account="4111 1111 1111 1111",
                expiry="1222",
                profile_id=profile_data["profileid"],
                name="Sam Carter",
                address="Red street 9",
                city="Denver",
                region="CO",
                postal="80014",
                phone="13332266550",
                email="user2@gmail.com"
            )
        """
        # Preventing the creation of an account with a given ID
        if profile_id is not None and "/" in profile_id:
            raise ValueError("profile_id parameter should not include account ID")

        data = utils.clean_data({
            "merchid": self.merchid,
            "account": account,
            "expiry": expiry,
            "defaultacct": defaultacct,

            "name": name,
            "company": company,
            "address": address,
            "address2": address2,
            "city": city,
            "region": region,
            "country": country,
            "postal": postal,
            "phone": phone,
            "email": email,

            "profile": profile_id,
            "cofpermission": cofpermission,

            "bankaba": bankaba,
            "auoptout": auoptout,
            "accttype": accttype,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result

    def update(
        self,
        *,
        profile: str,
        account: str,
        expiry: str,
        defaultacct: str = None,

        name: str = None,
        company: str = None,
        address: str = None,
        address2: str = None,
        city: str = None,
        region: str = None,
        country: str = None,
        postal: str = None,
        phone: str = None,
        email: str = None,

        cofpermission: str = None,

        bankaba: str = None,
        auoptout: str = None,
        accttype: str = None,
    ) -> Dict:
        """
        A PUT call to the profile endpoint updates existing account.

        :param profile:
            20-digit profile ID and 3-digit account ID string in the format
            <profile id>/<account id>.
        :param account:
            Can be:
                1) CardSecure Token - a token representing a payment account number.
                2) Clear text card number.
                3) Bank Account Number. When using BAN, the `bankaba` field is also required.
            Note: To use a stored profile, omit the account property and supply
            the profile ID in the profile field instead.
        :param expiry:
            Card expiration in one of the following formats
            MMYY, YYYYM (for single-digit months), YYYYMM, YYYYMMDD.
            Not required for eCheck (ACH) or digital wallet (for example, Apple Pay
            or Google Pay) payments.
        :param defaultacct:
            "Y" to assign as default account.

        :param name:
            Account holder's name, optional for credit cards and electronic checks (ACH).
        :param company:
            Account holder's company name.
        :param address:
            Account holder's street address, required for AVS verification.
        :param address2:
            Second address line (for example, apartment or suite number) if applicable.
        :param city:
            Account holder's city.
        :param region:
            Account holder's region, US State, Mexican State, Canadian Province.
        :param country:
            Account holder's country (2-character country code), defaults to "US".
            Required for all non-US addresses.
        :param postal:
            The account holder's postal code. If country is "US", must be 5 or 9 digits.
            Otherwise any alphanumeric string is accepted. Defaults to "55555"
            if not included in the request or stored profile.
        :param phone:
            Account holder's phone number. Optional for credit cards, but required
            for E-check/ACH authorizations.
        :param email:
            Account holder's email address.

        :param cofpermission:
            Optionally specifies whether or not the cardholder provided consent
            to store their payment details in a profile.
            Specify one of the following values:
                Y - The cardholder provided their consent to store and reuse their
                    payment details;
                N - The cardholder did not provide their consent.
            Defaults to N if not provided.

        :param bankaba:
            Bank routing (ABA) number. Required for eCheck (ACH) authorizations
            when a bank account number is provided in the account field.
            `bankaba` is not required if a CardSecure token (generated
            from the account/bankaba pair) is provided in the account field.
        :param auoptout:
            Specifies whether or not the profile is set to opt out of the CardPointe
            Account Updater service. Requires the merchant account to be enrolled
            in the Card Account Updater add-on.
            Specify one of the following values:
                Y - updates are not retrieved for this profile;
                N - updates are retrieved for this profile.
            Defaults to N if not provided.
        :param accttype:
            One of PPAL, PAID, GIFT, PDEBIT, otherwise not required.

        :raises ValueError: if account ID is not specified in the `profile` field.
        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Update account name
            api.profile.update(
                profile="13673043522000041712/1",
                account="4111 1111 1111 1111",
                expiry="1222",
                name="Peter Parker"
            )
        """
        # Prevent unintentional creation of new profile.
        # Note: it is still possible to create a new account if you specify
        # a non-existent account ID.
        if "/" not in profile:
            raise ValueError("A profile argument must include account ID")

        data = utils.clean_data({
            "merchid": self.merchid,
            "profile": profile,
            "account": account,
            "expiry": expiry,
            "defaultacct": defaultacct,
            "profileupdate": "Y",

            "name": name,
            "company": company,
            "address": address,
            "address2": address2,
            "city": city,
            "region": region,
            "country": country,
            "postal": postal,
            "phone": phone,
            "email": email,

            "cofpermission": cofpermission,

            "bankaba": bankaba,
            "auoptout": auoptout,
            "accttype": accttype,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("PUT", endpoint, json=data)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result

    def delete(
        self,
        *,
        profile: str,
    ) -> Dict:
        """
        A DELETE request to the profile endpoint deletes the stored data
        for the specified profile ID.

        If the profile includes more than one account, you can specify an account ID
        to delete data for a specific account. If you do not include an account ID,
        then data for all accounts in the profile is deleted.

        If a profile or an account within a profile is associated with a CardPointe
        Billing Plan, then deleting the account or profile also cancels and deletes
        the billing plan.

        :param profile:
            20-digit profile ID and (optional) 3-digit account ID string in the format
            <profile id>/<account id>.
            If the account ID is omitted, then all accounts in the profile are deleted.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Delete profile
            api.profile.delete(
                profile="13673043522000041712/1"
            )
        """
        if "/" in profile:
            profile_id, account_id = profile.split("/")
        else:
            profile_id, account_id = profile, ""

        endpoint = self.get_endpoint("{}/{}/{{merchid}}".format(
            profile_id,
            account_id if account_id is not None else ""
        ))
        response = self._client.request("DELETE", endpoint)
        result = response.json()

        if result["respstat"] != ResponseStatus.APPROVED:
            raise ApiError(result["resptext"], response=response)

        return result


class Signature(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/sigcap"

    def create(
        self,
        *,
        retref: str,
        signature: str = None,
    ) -> Dict:
        """
        This signature capture service augments an existing authorization record
        with the provided signature data. The signature can then be retrieved
        by an inquire request.

        :param retref:
            CardPointe retrieval reference number from authorization response.
        :param signature:
            JSON Encoded, Base64 Encoded, GZipped, BMP (200x100px) image.
            Omit to erase an associated signature.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Add signature
            api.signature.create(
                retref="293769756226",
                signature="..."
            )
        """
        data = utils.clean_data({
            "merchid": self.merchid,
            "retref": retref,
            "signature": signature,
        })

        endpoint = self.get_endpoint()
        response = self._client.request("POST", endpoint, json=data)
        result = response.json()

        if result["respcode"] != "02":
            raise ApiError(result["resptext"], response=response)

        return result


class BIN(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/bin"

    def get(
        self,
        *,
        token: str,
    ) -> Dict:
        """
        The BIN service allows you to use a CardSecure token to determine what type
        of payment card is being used. The first six (6) digits of a credit card
        are known as the Bank Identifier Number (BIN), also known as an Issuer
        Identification Number (IIN).

        :param token:
            The tokenized account number.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Get BIN
            api.bin.get(
                token="9418594164541111"
            )
        """
        endpoint = self.get_endpoint("{{merchid}}/{}".format(token))
        response = self._client.request("GET", endpoint)
        result = response.json()

        if not result["success"]:
            raise ApiError(result["errormsg"], response=response)

        return result


class Funding(ResourceBase):
    endpoint = "https://{site}.cardconnect.com/cardconnect/rest/funding"

    def get(
        self,
        *,
        date: str = None,
    ) -> Dict:
        """
        The funding endpoint provides merchant funding information and supplemental
        transaction and funding adjustment details. This information is provided
        by the host payment processing platform (for example, First Data Omaha).

        Funding data is only available for merchants with the funding service
        configured and enabled in the production environment.

        A request to the funding endpoint returns all available funding data
        for the merchant on the date specified, in an array of fundings,
        txns (transactions), adjustments, and chargebacks records.
        If no adjustment or chargeback data is present for the date specified,
        these arrays are not returned.

        :param date:
            Optional. Can be specified in the format MMDD to specify a day
            within the current calendar year, or YYYYMMDD to specify a date
            in a previous calendar year. If no date is specified, the service
            checks for any funding data that has not already been retrieved.

        :raises ApiError:
            if response's status code or response code indicates an error.

        Example:
            from cardpointe.gateway.api import GatewayAPI

            api = GatewayAPI(
                site="fts-uat",
                merchant_id="496160873888",
                username="testing",
                password="testing123"
            )

            # Inquire
            api.funding.get(
                date="20221024"
            )
        """
        path = "?merchid={merchid}"
        if date is not None:
            path += "&date={}".format(date)

        endpoint = self.get_endpoint(path)
        response = self._client.request("GET", endpoint)
        result = response.json()

        if "errormsg" in result:
            raise ApiError(result["errormsg"], response=response)

        return result
