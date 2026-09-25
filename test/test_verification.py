import pytest
from transaction_agent import VerificationResponse, Action, Belief, CostModel
from verification import (
    finalize_decision,
    request_verification,
    record_verification,
    calculate_expected_information_gain,
    select_best_verification_action,
)


def test_calculate_expected_information_gain_positive_for_uncertain_belief():
    uncertain_belief = Belief(legitimate_probability=0.50, fraudulent_probability=0.50)
    eig_sms = calculate_expected_information_gain(uncertain_belief, "sms_otp")
    assert eig_sms > 0.5  # Significant reduction in entropy


def test_select_best_verification_action_selects_highest_efficiency():
    uncertain_belief = Belief(legitimate_probability=0.50, fraudulent_probability=0.50)
    best_type, eig, efficiency = select_best_verification_action(uncertain_belief)
    # push_auth (cost=1.0) or sms_otp (cost=2.0) vs manual_review (cost=10.0)
    assert best_type in ["push_auth", "sms_otp"]
    assert efficiency > 0.10


def test_select_best_verification_action_returns_none_for_certain_belief():
    certain_belief = Belief(legitimate_probability=1.0, fraudulent_probability=0.0)
    best_type, eig, efficiency = select_best_verification_action(certain_belief)
    assert best_type is None
    assert eig == 0.0


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