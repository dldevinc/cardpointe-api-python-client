from ..utils import constants


@constants
class ResponseStatus:
    """ respstat """
    APPROVED = "A"
    RETRY = "B"
    DECLINED = "C"


@constants
class CVVResponse:
    """ cvvresp """
    # Valid CVV Match.
    VALID = "M"

    # Invalid CVV.
    INVALID = "N"

    # CVV Not Processed.
    NOT_PROCESSED = "P"

    # Merchant indicated that the CVV is not present on the card.
    NOT_PRESENT = "S"

    # Card issuer is not certified and/or has not provided Visa encryption keys.
    NOT_CERTIFIED = "U"

    # No response.
    NO_RESPONSE = "X"


@constants
class AVSResponse:
    """ avsresp """
    # The following response codes indicate that both the street address
    # and postal code have been verified.
    SUCCESSFUL = {"Y", "X", "F", "D"}

    # The following response codes indicate that only the street address,
    # or the postal code has been verified.
    PARTIALLY_SUCCESSFUL = {"A", "Z", "W", "P"}

    # The following response codes indicate that neither the street address
    # nor the postal code could be verified.
    UNSUCCESSFUL = {"N"}

    # The following response codes indicate that there was an issue in verifying
    # the address, or that the verification was not attempted.
    UNATTEMPTED = {"R", "S", "U", "G", ""}


@constants
class SettlementStatus:
    """ setlstat """
    # The authorization was approved, but the transaction has not yet been captured.
    AUTHORIZED = "Authorized"

    # The authorization was declined.
    DECLINED = "Declined"

    # The transaction was voided.
    VOIDED = "Voided"

    # The authorization was approved and captured but has not yet been sent for settlement.
    QUEUED_FOR_CAPTURE = "Queued for Capture"

    # The batch was sent for settlement, but the transaction was rejected for funding.
    REJECTED = "Rejected"

    # The batch for this transaction was transmitted and accepted for funding.
    ACCEPTED = "Accepted"

    # The authorization was a $0 auth for account validation.
    ZERO_AMOUNT = "Zero amount"

    # The order did not transmit for settlement due to unexpected or invalid order or item data.
    FORMAT_ERROR = "Format error"

    # The transaction was not settled due to a token decryption error.
    TOKEN_DECRYPT = "Token Decrypt"

    # Vantiv only.
    # PIN debit transactions are settled by Vantiv, and are not submitted with the batch for settlement.
    PIN_DEBIT = "Pin Debit"

    # First Data North and Rapid Connect only.
    # The batch for this transaction was transmitted for settlement, and the transaction
    # was placed under review because the amount exceeded a configured threshold.
    UNDER_REVIEW = "Amount under review"


@constants
class CardType:
    """ product """
    AMEX = "A"
    DISCOVER = "D"
    MASTERCARD = "M"
    NON_BRANDED = "N"
    VISA = "V"
