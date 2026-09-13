from datetime import datetime

from transaction_agent import (
    Transaction,
    ProfileSummary,
    EvidenceDirection,
    VerificationResponse,
    Verification,
)

from evidence import (
    check_amount_evidence,
    extract_verification_evidence,
)


def test_large_amount_is_fraud_supporting():

    profile = ProfileSummary(
        customer_id="C001",
        typical_amount=500,
        common_merchants=["Amazon"],
        typical_locations=["Bangalore"],
        typical_transaction_hours=[10, 12],
    )

    transaction = Transaction(
        transaction_id="T001",
        customer_id="C001",
        amount=1000,
        merchant="Amazon",
        timestamp=datetime(2026, 9, 5, 12, 30),
        location="Bangalore",
    )

    evidence = check_amount_evidence(transaction, profile)

    assert evidence.name == "large_amount"
    assert evidence.direction == EvidenceDirection.SUPPORTS_FRAUDULENT


def test_confirmed_verification_supports_legitimate():

    verification = Verification(
        response=VerificationResponse.CONFIRMED
    )

    evidence = extract_verification_evidence(verification)

    assert evidence.name == "customer_confirms"
    assert evidence.direction == EvidenceDirection.SUPPORTS_LEGITIMATE


def test_denied_verification_supports_fraudulent():

    verification = Verification(
        response=VerificationResponse.DENIED
    )

    evidence = extract_verification_evidence(verification)

    assert evidence.name == "customer_denies"
    assert evidence.direction == EvidenceDirection.SUPPORTS_FRAUDULENT