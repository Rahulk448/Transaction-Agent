import pytest
from transaction_agent import Action, Belief, CostModel
from decision import (
    make_decision,
    derive_binary_threshold,
    derive_hold_thresholds,
)


def test_derive_binary_threshold_default_cost_model():
    p_star = derive_binary_threshold()
    # 8.0 / (8.0 + 10.0) = 8 / 18 = 0.4444444...
    assert p_star == pytest.approx(8.0 / 18.0)


def test_derive_hold_thresholds_default_cost_model():
    p_low, p_high = derive_hold_thresholds()
    assert p_low == pytest.approx(0.20)
    assert p_high == pytest.approx(0.75)


def test_derive_hold_thresholds_high_cost_hold_returns_none():
    high_hold_cost = CostModel(
        approve_legitimate=0,
        approve_fraudulent=10,
        hold_legitimate=9,
        hold_fraudulent=9,
        stop_legitimate=8,
        stop_fraudulent=0,
    )
    p_low, p_high = derive_hold_thresholds(high_hold_cost)
    assert p_low is None
    assert p_high is None



def test_decision_approves_when_legitimate_is_high():
    belief = Belief(
        fraudulent_probability=0.10,
        legitimate_probability=0.90,
    )

    cost_model = CostModel(
        approve_legitimate=0,
        approve_fraudulent=10,
        hold_legitimate=6,
        hold_fraudulent=4,
        stop_legitimate=8,
        stop_fraudulent=0,
    )

    decision = make_decision(belief, cost_model)

    assert decision.action == Action.APPROVE


def test_default_cost_model_approves_low_fraud_probability():
    belief = Belief(fraudulent_probability=0.05, legitimate_probability=0.95)
    decision = make_decision(belief)
    assert decision.action == Action.APPROVE


def test_default_cost_model_holds_intermediate_uncertain_belief():
    belief = Belief(fraudulent_probability=0.40, legitimate_probability=0.60)
    decision = make_decision(belief)
    assert decision.action == Action.HOLD


def test_default_cost_model_stops_high_fraud_probability():
    belief = Belief(fraudulent_probability=0.85, legitimate_probability=0.15)
    decision = make_decision(belief)
    assert decision.action == Action.STOP