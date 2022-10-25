# cardpointe-api-python-client

Unofficial Python client library for CardPointe Gateway and CardSecure APIs.

[![PyPI](https://img.shields.io/pypi/v/cardpointe-api-python-client.svg)](https://pypi.org/project/cardpointe-api-python-client/)
[![Build Status](https://github.com/dldevinc/cardpointe-api-python-client/actions/workflows/tests.yml/badge.svg)](https://github.com/dldevinc/cardpointe-api-python-client)
[![Software license](https://img.shields.io/pypi/l/cardpointe-api-python-client.svg)](https://pypi.org/project/cardpointe-api-python-client/)

## Compatibility

-   `python` >= 3.7

## Installation

Install the latest release with pip:

```shell
pip install cardpointe-api-python-client
```

## Example Usage

### CardPointe Gateway API

```python
from cardpointe.gateway.api import GatewayAPI

api = GatewayAPI(
    site="fts-uat",
    merchant_id="496160873888",
    username="testing",
    password="testing123"
)

# Inquire Merchant
response = api.inquireMerchant.get()

# Authorization & capture
response = api.authorization.create(
    amount="2.50",
    account="4111 1111 1111 1111",
    expiry="1225",
    cvv2="123",

    name="John Smith",
    city="Denver",
    region="CO",
    postal="80014",
    email="john@smith.com",

    ecomind="E",
    capture="Y",
    userfields={
        "invoice": 12345,
        "user_id": 3
    }
)
```

Check out the table below for the full list of available services:

| Service                                                                                     | Examples                                                                                                      |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [Inquire Merchant](https://developer.cardpointe.com/cardconnect-api#inquire-merchant)       | `api.inquireMerchant.get()`                                                                                   |
| [Authorization](https://developer.cardpointe.com/cardconnect-api#authorization)             | `api.authorization.create(...)`                                                                               |
| [Capture](https://developer.cardpointe.com/cardconnect-api#capture)                         | `api.capture.create(...)`                                                                                     |
| [Inquire](https://developer.cardpointe.com/cardconnect-api#inquire)                         | `api.inquire.get(...)`                                                                                        |
| [Inquire By Order ID](https://developer.cardpointe.com/cardconnect-api#inquire-by-order-id) | `api.inquireByOrderId.get(...)`                                                                               |
| [Void](https://developer.cardpointe.com/cardconnect-api#void)                               | `api.void.create(...)`                                                                                        |
| [Void By Order ID](https://developer.cardpointe.com/cardconnect-api#void-by-order-id)       | `api.voidByOrderId.create(...)`                                                                               |
| [Refund](https://developer.cardpointe.com/cardconnect-api#refund)                           | `api.refund.create(...)`                                                                                      |
| [Profile](https://developer.cardpointe.com/cardconnect-api#profile)                         | `api.profile.get(...)`<br>`api.profile.create(...)`<br>`api.profile.update(...)`<br>`api.profile.delete(...)` |
| [Signature Capture](https://developer.cardpointe.com/cardconnect-api#signature-capture)     | `api.signature.create(...)`                                                                                   |
| [BIN](https://developer.cardpointe.com/cardconnect-api#bin)                                 | `api.bin.get(...)`                                                                                            |
| [Funding](https://developer.cardpointe.com/cardconnect-api#funding)                         | `api.funding.get(...)`                                                                                        |

### CardPointe CardSecure API

```python
from cardpointe.cardsecure.api import CardSecureAPI

api = CardSecureAPI(
    site="fts-uat",
    merchant_id="496160873888",
    username="testing",
    password="testing123"
)

response = api.tokenize.create(
    account="4111 1111 1111 1111",
    expiry="1225",
    cvv="123"
)
```

Check out the table below for the full list of available services:

| Service                                                              | Examples                                                 |
| -------------------------------------------------------------------- | -------------------------------------------------------- |
| [Tokenize](https://developer.cardpointe.com/cardsecure-api#tokenize) | `api.tokenize.create(...)`<br>`api.tokenize.update(...)` |
| [Echo](https://developer.cardpointe.com/cardsecure-api#echo)         | `api.echo.create(...)`                                   |

## Links

-   [Gateway API Docs](https://developer.cardpointe.com/cardconnect-api)
-   [CardSecure API Docs](https://developer.cardpointe.com/cardsecure-api)
