from transaction_agent import VerificationResponse
from verification import finalize_decision, request_verification, record_verification
from transaction_agent import Action, Belief, CostModel

def test_request_verification_creates_pending_verification():
    pending = request_verification("T001")

    assert pending.transaction_id == "T001"


def test_record_confirmed_verification():
    verification = record_verification(
        VerificationResponse.CONFIRMED
    )

    assert verification.response == VerificationResponse.CONFIRMED


def test_record_denied_verification():
    verification = record_verification(
        VerificationResponse.DENIED
    )

    assert verification.response == VerificationResponse.DENIED

def test_confirmed_verification_can_finalize_decision():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    verification = record_verification(
        VerificationResponse.CONFIRMED
    )

    cost_model = CostModel(
        approve_legitimate=0,
        approve_fraudulent=10,
        hold_legitimate=6,
        hold_fraudulent=4,
        stop_legitimate=8,
        stop_fraudulent=0,
    )

    decision = finalize_decision(
        belief,
        verification,
        cost_model,
    )

    assert decision.action == Action.APPROVE