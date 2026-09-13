from datetime import datetime

from transaction_agent import CustomerProfile, HistoricalTransaction
from profile import (
    build_profile_summary,
    calculate_common_merchants,
    calculate_typical_amount,
    calculate_typical_locations,
    calculate_typical_transaction_hours,
)


def make_test_profile() -> CustomerProfile:
    transactions = [
        HistoricalTransaction(
            transaction_id="H001",
            customer_id="C001",
            amount=100.0,
            merchant="Amazon",
            timestamp=datetime(2026, 1, 1, 10, 30),
            location="Bangalore",
        ),
        HistoricalTransaction(
            transaction_id="H002",
            customer_id="C001",
            amount=300.0,
            merchant="Flipkart",
            timestamp=datetime(2026, 1, 2, 14, 15),
            location="Bangalore",
        ),
        HistoricalTransaction(
            transaction_id="H003",
            customer_id="C001",
            amount=200.0,
            merchant="Amazon",
            timestamp=datetime(2026, 1, 3, 10, 45),
            location="Mumbai",
        ),
    ]

    return CustomerProfile(
        customer_id="C001",
        historical_transactions=transactions,
    )


def test_profile_summary():
    profile = make_test_profile()

    summary = build_profile_summary(profile)

    assert summary.customer_id == "C001"
    assert summary.typical_amount == 200.0
    assert summary.common_merchants == ["Amazon", "Flipkart"]
    assert summary.typical_locations == ["Bangalore", "Mumbai"]
    assert summary.typical_transaction_hours == [10, 14]