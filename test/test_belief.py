import pytest

from transaction_agent import Belief, Evidence, EvidenceDirection
from belief import update_belief


def test_large_amount_updates_belief_toward_fraud():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="large_amount",
        direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(0.14285714285714285)
    assert updated.legitimate_probability == pytest.approx(0.8571428571428571)


def test_customer_confirmation_updates_belief_toward_legitimate():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="customer_confirms",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(0.005813953488372094)
    assert updated.legitimate_probability == pytest.approx(0.9941860465116279)


def test_customer_denial_updates_belief_toward_fraud():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="customer_denies",
        direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(0.6785714285714286)
    assert updated.legitimate_probability == pytest.approx(0.32142857142857145)


def test_amount_consistent_updates_belief_toward_legitimate():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="amount_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(7 / 79)
    assert updated.legitimate_probability == pytest.approx(72 / 79)


def test_unusual_location_updates_belief_toward_fraud():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="unusual_location",
        direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(0.25)
    assert updated.legitimate_probability == pytest.approx(0.75)


def test_location_consistent_updates_belief_toward_legitimate():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    evidence = Evidence(
        name="location_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )

    updated = update_belief(belief, evidence)

    assert updated.fraudulent_probability == pytest.approx(7 / 88)
    assert updated.legitimate_probability == pytest.approx(81 / 88)