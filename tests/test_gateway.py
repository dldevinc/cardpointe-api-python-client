from decimal import Decimal
from unittest.mock import patch

from cardpointe.gateway.api import GatewayAPI

from .mocks import mock_response

api = GatewayAPI(
    site="fts-uat",
    merchant_id="496160873888",
    username="testing",
    password="testing123"
)


@patch("requests.request", side_effect=mock_response({}))
def test_inquire_merchant(mock_class):
    response = api.inquireMerchant.get()
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/inquireMerchant/496160873888"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_authorization(mock_class):
    response = api.authorization.create(
        amount="2.01",
        account="4111 1111 1111 1111",
        expiry="1222",
        cvv2="123",
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/auth"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "amount": "2.01",
        "account": "4111 1111 1111 1111",
        "expiry": "1222",
        "cvv2": "123"
    }


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_capture(mock_class):
    response = api.capture.create(
        retref="296072706652",
        amount=Decimal("1.25")
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/capture"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "retref": "296072706652",
        "amount": "1.25",
    }


@patch("requests.request", side_effect=mock_response({
    "account": "9418594164541111",
    "respstat": "A"
}))
def test_inquire(mock_class):
    response = api.inquire.get(
        retref="296072706652"
    )
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/inquire/296072706652/496160873888"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({
    "account": "9418594164541111",
    "respstat": "A"
}))
def test_inquire_by_orderid(mock_class):
    response = api.inquireByOrderId.get(
        orderid="771",
        set_=1
    )
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/inquireByOrderid/771/496160873888/1"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_void(mock_class):
    response = api.void.create(
        retref="296072706652"
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/void"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "retref": "296072706652"
    }


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_void_by_orderid(mock_class):
    response = api.voidByOrderId.create(
        orderid="772"
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/voidByOrderId"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "orderid": "772"
    }


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_refund(mock_class):
    response = api.refund.create(
        retref="296072706652"
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/refund"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "retref": "296072706652"
    }


@patch("requests.request", side_effect=mock_response([{
    "respstat": "A"
}]))
def test_get_profile(mock_class):
    response = api.profile.get(
        profile="13673043522000041712/1",
    )
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/profile/13673043522000041712/1/496160873888"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_create_profile(mock_class):
    response = api.profile.create(
        account="4111 1111 1111 1111",
        expiry="1222",
        name="John Snow",
        address="Green street 16",
        city="Denver",
        region="CO",
        postal="80014",
        phone="12345678900",
        email="user@gmail.com",
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/profile"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "account": "4111 1111 1111 1111",
        "expiry": "1222",
        "name": "John Snow",
        "address": "Green street 16",
        "city": "Denver",
        "region": "CO",
        "postal": "80014",
        "phone": "12345678900",
        "email": "user@gmail.com",
    }


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_update_profile(mock_class):
    response = api.profile.update(
        profile="13673043522000041712/1",
        account="4111 1111 1111 1111",
        expiry="1222",
        name="Peter Parker",
    )
    assert response.method == "PUT"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/profile"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "profile": "13673043522000041712/1",
        "account": "4111 1111 1111 1111",
        "expiry": "1222",
        "profileupdate": "Y",
        "name": "Peter Parker",
    }


@patch("requests.request", side_effect=mock_response({
    "respstat": "A"
}))
def test_delete_profile(mock_class):
    response = api.profile.delete(
        profile="13673043522000041712/1",
    )
    assert response.method == "DELETE"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/profile/13673043522000041712/1/496160873888"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({
    "respcode": "02"
}))
def test_add_signature(mock_class):
    response = api.signature.create(
        retref="296072706652",
        signature=""
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/sigcap"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "merchid": "496160873888",
        "retref": "296072706652",
        "signature": "",
    }


@patch("requests.request", side_effect=mock_response({
    "success": True
}))
def test_get_bin(mock_class):
    response = api.bin.get(
        token="9418594164541111",
    )
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/bin/496160873888/9418594164541111"
    assert response.kwargs["auth"] == ("testing", "testing123")


@patch("requests.request", side_effect=mock_response({}))
def test_funding(mock_class):
    response = api.funding.get(
        date="20221024"
    )
    assert response.method == "GET"
    assert response.url == "https://fts-uat.cardconnect.com/cardconnect/rest/funding?merchid=496160873888&date=20221024"
    assert response.kwargs["auth"] == ("testing", "testing123")

