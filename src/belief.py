from transaction_agent import (
    Belief,
    Evidence,
    EvidenceDirection,
)


LIKELIHOODS = {
    "large_amount": {"fraudulent": 0.30, "legitimate": 0.20},
    "amount_consistent": {"fraudulent": 0.70, "legitimate": 0.80},
    "new_merchant": {"fraudulent": 0.30, "legitimate": 0.15},
    "merchant_consistent": {"fraudulent": 0.70, "legitimate": 0.85},
    "unusual_location": {"fraudulent": 0.30, "legitimate": 0.10},
    "location_consistent": {"fraudulent": 0.70, "legitimate": 0.90},
    "unusual_time": {"fraudulent": 0.40, "legitimate": 0.10},
    "time_consistent": {"fraudulent": 0.60, "legitimate": 0.90},
    "customer_confirms": {"fraudulent": 0.05, "legitimate": 0.95},
    "customer_denies": {"fraudulent": 0.95, "legitimate": 0.05},
}


def update_belief(
    belief: Belief,
    evidence: Evidence,
) -> Belief:
    likelihood = LIKELIHOODS.get(evidence.name)

    if likelihood is None:
        return belief

    prior_fraud = belief.fraudulent_probability
    prior_legitimate = belief.legitimate_probability

    fraud_likelihood = likelihood["fraudulent"]
    legitimate_likelihood = likelihood["legitimate"]

    fraud_weight = prior_fraud * fraud_likelihood
    legitimate_weight = prior_legitimate * legitimate_likelihood

    total = fraud_weight + legitimate_weight

    if total == 0:
        return belief

    posterior_fraud = fraud_weight / total
    posterior_legitimate = legitimate_weight / total

    return Belief(
        fraudulent_probability=posterior_fraud,
        legitimate_probability=posterior_legitimate,
    )