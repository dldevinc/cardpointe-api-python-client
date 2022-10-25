from unittest.mock import patch

from cardpointe.cardsecure.api import CardSecureAPI

from .mocks import mock_response

api = CardSecureAPI(
    site="fts-uat",
    merchant_id="496160873888",
    username="testing",
    password="testing123"
)


@patch("requests.request", side_effect=mock_response({
    "errorcode": 0
}))
def test_tokenize(mock_class):
    response = api.tokenize.create(
        account="4111 1111 1111 1111",
        expiry="1222",
        cvv="123",
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardsecure/api/v1/ccn/tokenize"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "account": "4111 1111 1111 1111",
        "expiry": "1222",
        "cvv": "123"
    }


@patch("requests.request", side_effect=mock_response({
    "errorcode": 0
}))
def test_update_token(mock_class):
    response = api.tokenize.update(
        account="9418594164541111",
        expiry="1222",
        cvv="123",
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardsecure/api/v1/ccn/tokenize"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "account": "9418594164541111",
        "expiry": "1222",
        "cvv": "123"
    }


@patch("requests.request", side_effect=mock_response({
    "errorcode": 0
}))
def test_echo(mock_class):
    response = api.echo.create(
        message="Hello"
    )
    assert response.method == "POST"
    assert response.url == "https://fts-uat.cardconnect.com/cardsecure/api/v1/echo"
    assert response.kwargs["auth"] == ("testing", "testing123")
    assert response.kwargs["json"] == {
        "message": "Hello"
    }
