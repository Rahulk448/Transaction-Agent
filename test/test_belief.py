import pytest

from transaction_agent import Belief, Evidence, EvidenceDirection
from belief import update_belief, calculate_entropy, calculate_kl_divergence


def test_calculate_entropy_50_50_returns_one_bit():
    belief = Belief(legitimate_probability=0.50, fraudulent_probability=0.50)
    assert calculate_entropy(belief) == pytest.approx(1.0)


def test_calculate_entropy_certainty_returns_zero_bits():
    belief = Belief(legitimate_probability=1.0, fraudulent_probability=0.0)
    assert calculate_entropy(belief) == pytest.approx(0.0)


def test_calculate_entropy_prior_90_10():
    belief = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    # H = -0.9 log2(0.9) - 0.1 log2(0.1) approx 0.46899583
    assert calculate_entropy(belief) == pytest.approx(0.46899583)


def test_calculate_kl_divergence_identical_beliefs_returns_zero():
    prior = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    posterior = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    assert calculate_kl_divergence(prior, posterior) == pytest.approx(0.0)


def test_calculate_kl_divergence_shifted_belief():
    prior = Belief(legitimate_probability=0.90, fraudulent_probability=0.10)
    posterior = Belief(legitimate_probability=0.70, fraudulent_probability=0.30)
    kl = calculate_kl_divergence(prior, posterior)
    assert kl > 0.0
    assert kl == pytest.approx(0.2217, abs=1e-3)



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