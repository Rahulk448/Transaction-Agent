from transaction_agent import (
    Verification,
    VerificationResponse,
    PendingVerification,
    Belief,
    CostModel,
    Decision,
)

from evidence import extract_verification_evidence
from belief import update_belief
from decision import make_decision, DEFAULT_COST_MODEL


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