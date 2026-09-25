import math

from transaction_agent import (
    Belief,
    Evidence,
    EvidenceDirection,
)


def calculate_entropy(belief: Belief) -> float:
    """Calculate the Shannon entropy of a belief distribution in bits.

    H(P) = - sum(p * log2(p)) for p in [p_legit, p_fraud]
    """
    entropy = 0.0
    probs = [belief.legitimate_probability, belief.fraudulent_probability]
    for p in probs:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def calculate_kl_divergence(prior: Belief, posterior: Belief) -> float:
    """Calculate the Kullback-Leibler divergence D_KL(posterior || prior) in bits.

    D_KL(Q || P) = sum(Q(x) * log2(Q(x) / P(x)))
    where Q is posterior and P is prior.
    """
    kl = 0.0
    pairs = [
        (posterior.legitimate_probability, prior.legitimate_probability),
        (posterior.fraudulent_probability, prior.fraudulent_probability),
    ]
    for q, p in pairs:
        if q > 0:
            if p <= 0:
                return float("inf")
            kl += q * math.log2(q / p)
    return kl




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