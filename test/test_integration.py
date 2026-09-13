from datetime import datetime
import pytest

from transaction_agent import (
    Action,
    Belief,
    CostModel,
    ProfileSummary,
    Transaction,
    VerificationResponse,
)
from evidence import extract_evidence
from belief import update_belief
from decision import make_decision, calculate_expected_cost, DEFAULT_COST_MODEL
from verification import (
    request_verification,
    record_verification,
    finalize_decision,
)
from data_loader import (
    load_historical_transactions,
    group_by_customer,
    build_customer_profiles,
    build_all_profile_summaries,
)


@pytest.fixture
def default_cost_model() -> CostModel:
    return DEFAULT_COST_MODEL


@pytest.fixture
def c001_profile() -> ProfileSummary:
    return ProfileSummary(
        customer_id="C001",
        typical_amount=1088.0,
        common_merchants=["Flipkart", "Amazon", "Big Bazaar"],
        typical_locations=["Bangalore"],
        typical_transaction_hours=[10, 12, 15, 18, 14, 11, 17, 19, 13],
    )


def test_consistent_transaction_end_to_end_approves(default_cost_model, c001_profile):
    """Smoke test: A transaction matching customer profile updates belief toward legitimate and APPROVEs."""
    transaction = Transaction(
        transaction_id="TC01-INTEGRATION",
        customer_id="C001",
        amount=1200.0,
        merchant="Amazon",
        timestamp=datetime(2026, 9, 8, 14, 0),
        location="Bangalore",
    )

    # 1. Evidence extraction
    evidence_list = extract_evidence(transaction, c001_profile)
    evidence_names = [e.name for e in evidence_list]
    assert evidence_names == [
        "amount_consistent",
        "merchant_consistent",
        "location_consistent",
        "time_consistent",
    ]

    # 2. Sequential Bayesian belief updating
    belief = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    for ev in evidence_list:
        belief = update_belief(belief, ev)

    # Mathematical expected posterior:
    # fraud weight: 0.10 * 0.70 * 0.70 * 0.70 * 0.60 = 0.02058
    # legit weight: 0.90 * 0.80 * 0.85 * 0.90 * 0.90 = 0.49572
    # total: 0.5163
    # posterior fraud: 0.02058 / 0.5163 = 0.0398605
    # posterior legit: 0.49572 / 0.5163 = 0.9601394
    assert belief.legitimate_probability == pytest.approx(0.96013945, rel=1e-4)
    assert belief.fraudulent_probability == pytest.approx(0.03986054, rel=1e-4)

    # 3. Expected cost calculation & decision
    decision = make_decision(belief, default_cost_model)
    assert decision.action == Action.APPROVE
    assert decision.expected_cost == pytest.approx(
        calculate_expected_cost(belief, Action.APPROVE, default_cost_model)
    )


def test_all_anomalies_transaction_end_to_end_stops(default_cost_model, c001_profile):
    """A transaction with anomalies across all fields updates belief toward fraud and STOPs."""
    transaction = Transaction(
        transaction_id="TC02-INTEGRATION",
        customer_id="C001",
        amount=92000.0,
        merchant="UnknownCryptoExchange",
        timestamp=datetime(2026, 9, 8, 4, 0),
        location="UnknownCity",
    )

    # 1. Evidence extraction
    evidence_list = extract_evidence(transaction, c001_profile)
    evidence_names = [e.name for e in evidence_list]
    assert evidence_names == [
        "large_amount",
        "new_merchant",
        "unusual_location",
        "unusual_time",
    ]

    # 2. Sequential Bayesian belief updating
    belief = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    for ev in evidence_list:
        belief = update_belief(belief, ev)

    # Mathematical expected posterior:
    # fraud weight: 0.10 * 0.30 * 0.30 * 0.30 * 0.40 = 0.00108
    # legit weight: 0.90 * 0.20 * 0.15 * 0.10 * 0.10 = 0.00027
    # total: 0.00135
    # fraud: 0.00108 / 0.00135 = 0.80
    # legit: 0.00027 / 0.00135 = 0.20
    assert belief.fraudulent_probability == pytest.approx(0.80)
    assert belief.legitimate_probability == pytest.approx(0.20)

    # 3. Expected cost decision
    decision = make_decision(belief, default_cost_model)
    assert decision.action == Action.STOP


def test_hold_and_verification_pipeline(default_cost_model):
    """Verify that when a decision is HOLD, customer verification updates belief and finalizes decision."""
    ambiguous_belief = Belief(legitimate_probability=0.50, fraudulent_probability=0.50)
    initial_decision = make_decision(ambiguous_belief, default_cost_model)
    assert initial_decision.action == Action.HOLD

    # Initiate verification
    pending = request_verification("TX-HOLD-1")
    assert pending.transaction_id == "TX-HOLD-1"

    # Branch A: Customer CONFIRMED
    confirmed = record_verification(VerificationResponse.CONFIRMED)
    final_confirmed_decision = finalize_decision(ambiguous_belief, confirmed, default_cost_model)
    assert final_confirmed_decision.action == Action.APPROVE

    # Branch B: Customer DENIED
    denied = record_verification(VerificationResponse.DENIED)
    final_denied_decision = finalize_decision(ambiguous_belief, denied, default_cost_model)
    assert final_denied_decision.action == Action.STOP


def test_end_to_end_hold_and_verification_flow(default_cost_model, c001_profile):
    """Transaction with mixed evidence lands in HOLD, then verification resolves to APPROVE or STOP."""
    # Unusual time and new merchant, but usual amount and usual location
    tx = Transaction(
        transaction_id="TX-HOLD-E2E",
        customer_id="C001",
        amount=1200.0,
        merchant="NewUnknownMerchant",
        timestamp=datetime(2026, 9, 8, 4, 0),  # 4am is unusual for C001
        location="Bangalore",
    )

    evidence_list = extract_evidence(tx, c001_profile)
    belief = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    for ev in evidence_list:
        belief = update_belief(belief, ev)

    # Mixed signals result in intermediate fraud belief (~37.7%)
    assert 0.20 < belief.fraudulent_probability < 0.75

    # Initial decision must be HOLD
    decision = make_decision(belief, default_cost_model)
    assert decision.action == Action.HOLD

    # If customer confirms: resolves to APPROVE
    confirmed = record_verification(VerificationResponse.CONFIRMED)
    final_decision_confirmed = finalize_decision(belief, confirmed, default_cost_model)
    assert final_decision_confirmed.action == Action.APPROVE

    # If customer denies: resolves to STOP
    denied = record_verification(VerificationResponse.DENIED)
    final_decision_denied = finalize_decision(belief, denied, default_cost_model)
    assert final_decision_denied.action == Action.STOP



def test_real_historical_dataset_c001_smoke_test(default_cost_model):
    """Loads actual historical CSV, extracts C001 profile, runs smoke test end-to-end."""
    transactions = load_historical_transactions("data/synthetic_historical_transactions.csv")
    grouped = group_by_customer(transactions)
    profiles = build_customer_profiles(grouped)
    summaries = build_all_profile_summaries(profiles)

    # Find C001
    c001 = next(s for s in summaries if s.customer_id == "C001")
    assert c001.customer_id == "C001"

    test_tx = Transaction(
        transaction_id="TC01-SMOKE",
        customer_id="C001",
        amount=1200.0,
        merchant="Amazon",
        timestamp=datetime(2026, 9, 8, 14, 0),
        location="Bangalore",
    )

    evidence_list = extract_evidence(test_tx, c001)
    belief = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    for ev in evidence_list:
        belief = update_belief(belief, ev)

    decision = make_decision(belief, default_cost_model)
    assert decision.action == Action.APPROVE
    assert belief.legitimate_probability > 0.95
