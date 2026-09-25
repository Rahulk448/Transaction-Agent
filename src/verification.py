from transaction_agent import (
    Verification,
    VerificationResponse,
    PendingVerification,
    Belief,
    CostModel,
    Decision,
)

from evidence import extract_verification_evidence
from belief import update_belief, calculate_entropy
from decision import make_decision, DEFAULT_COST_MODEL

VERIFICATION_CATALOG = {
    "push_auth": {
        "cost": 1.0,
        "confirms_given_legit": 0.90,
        "denies_given_fraud": 0.90,
    },
    "sms_otp": {
        "cost": 2.0,
        "confirms_given_legit": 0.95,
        "denies_given_fraud": 0.95,
    },
    "manual_review": {
        "cost": 10.0,
        "confirms_given_legit": 0.99,
        "denies_given_fraud": 0.99,
    },
}


def calculate_expected_information_gain(
    belief: Belief,
    verification_type: str = "sms_otp",
) -> float:
    """Calculate the Expected Information Gain (EIG) in bits for a verification check.

    EIG(V) = H(start) - E[H(after V)]
    """
    config = VERIFICATION_CATALOG.get(verification_type)
    if config is None:
        return 0.0

    p_legit_start = belief.legitimate_probability
    p_fraud_start = belief.fraudulent_probability
    h_start = calculate_entropy(belief)

    p_conf_given_legit = config["confirms_given_legit"]
    p_deny_given_fraud = config["denies_given_fraud"]

    p_conf_given_fraud = 1.0 - p_deny_given_fraud
    p_deny_given_legit = 1.0 - p_conf_given_legit

    # Outcome 1: Customer Confirms
    p_confirms = (p_legit_start * p_conf_given_legit) + (p_fraud_start * p_conf_given_fraud)
    if p_confirms > 0:
        p_legit_if_conf = (p_legit_start * p_conf_given_legit) / p_confirms
        p_fraud_if_conf = (p_fraud_start * p_conf_given_fraud) / p_confirms
        h_confirms = calculate_entropy(Belief(legitimate_probability=p_legit_if_conf, fraudulent_probability=p_fraud_if_conf))
    else:
        h_confirms = 0.0

    # Outcome 2: Customer Denies
    p_denies = (p_legit_start * p_deny_given_legit) + (p_fraud_start * p_deny_given_fraud)
    if p_denies > 0:
        p_legit_if_deny = (p_legit_start * p_deny_given_legit) / p_denies
        p_fraud_if_deny = (p_fraud_start * p_deny_given_fraud) / p_denies
        h_denies = calculate_entropy(Belief(legitimate_probability=p_legit_if_deny, fraudulent_probability=p_fraud_if_deny))
    else:
        h_denies = 0.0

    h_expected = (p_confirms * h_confirms) + (p_denies * h_denies)
    return max(0.0, h_start - h_expected)


def select_best_verification_action(
    belief: Belief,
    available_types: list[str] | None = None,
    min_efficiency: float = 0.05,
) -> tuple[str | None, float, float]:
    """Select the verification action with the highest Information Efficiency (EIG / Cost).

    Returns (best_type, best_eig, best_efficiency).
    """
    if available_types is None:
        available_types = list(VERIFICATION_CATALOG.keys())

    best_type = None
    best_eig = 0.0
    best_efficiency = 0.0

    for v_type in available_types:
        config = VERIFICATION_CATALOG.get(v_type)
        if not config:
            continue
        cost = config["cost"]
        eig = calculate_expected_information_gain(belief, v_type)
        efficiency = eig / cost if cost > 0 else 0.0

        if efficiency > best_efficiency and efficiency >= min_efficiency:
            best_type = v_type
            best_eig = eig
            best_efficiency = efficiency

    return best_type, best_eig, best_efficiency



def request_verification(transaction_id: str) -> PendingVerification:
    """Create a pending verification request for a transaction."""
    return PendingVerification(
        transaction_id=transaction_id,
    )


def record_verification(response: VerificationResponse) -> Verification:
    """Record the customer's verification response."""
    return Verification(
        response=response,
    )


def finalize_decision(
    belief: Belief,
    verification: Verification,
    cost_model: CostModel = DEFAULT_COST_MODEL,
) -> Decision:
    """Update belief using verification and make the final decision."""

    verification_evidence = extract_verification_evidence(
        verification
    )

    updated_belief = update_belief(
        belief,
        verification_evidence,
    )

    return make_decision(
        updated_belief,
        cost_model,
    )