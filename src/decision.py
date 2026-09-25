from transaction_agent import Action, Belief, CostModel, Decision

DEFAULT_COST_MODEL = CostModel(
    approve_legitimate=0.0,
    approve_fraudulent=10.0,
    hold_legitimate=2.0,
    hold_fraudulent=2.0,
    stop_legitimate=8.0,
    stop_fraudulent=0.0,
)


def derive_binary_threshold(cost_model: CostModel = DEFAULT_COST_MODEL) -> float:
    """Derive binary decision threshold p* between APPROVE and STOP.

    p* = C_FP / (C_FP + C_FN)
    where C_FP is cost of stopping legitimate, and C_FN is cost of approving fraud.
    """
    c_fp = cost_model.stop_legitimate - cost_model.approve_legitimate
    c_fn = cost_model.approve_fraudulent - cost_model.stop_fraudulent

    denom = c_fp + c_fn
    if denom == 0:
        return 0.5
    return c_fp / denom


def derive_hold_thresholds(
    cost_model: CostModel = DEFAULT_COST_MODEL,
) -> tuple[float | None, float | None]:
    """Derive lower and upper probability thresholds where HOLD has the lowest expected cost.

    Returns (p_low, p_high). If HOLD is never optimal, returns (None, None).
    """
    # Lower threshold: EC(APPROVE) = EC(HOLD)
    # (1-p)*c_app_leg + p*c_app_fr = (1-p)*c_hold_leg + p*c_hold_fr
    num_low = cost_model.hold_legitimate - cost_model.approve_legitimate
    denom_low = (cost_model.approve_fraudulent - cost_model.hold_fraudulent) + num_low

    if denom_low <= 0:
        return None, None
    p_low = num_low / denom_low

    # Upper threshold: EC(HOLD) = EC(STOP)
    # (1-p)*c_hold_leg + p*c_hold_fr = (1-p)*c_stop_leg + p*c_stop_fr
    num_high = cost_model.stop_legitimate - cost_model.hold_legitimate
    denom_high = num_high + (cost_model.hold_fraudulent - cost_model.stop_fraudulent)

    if denom_high <= 0:
        return None, None
    p_high = num_high / denom_high

    if p_low >= p_high:
        # HOLD cost is too high; HOLD is never optimal
        return None, None

    return p_low, p_high



def calculate_expected_cost(
    belief: Belief,
    action: Action,
    cost_model: CostModel = DEFAULT_COST_MODEL,
) -> float:

    if action == Action.APPROVE:
        legitimate_cost = cost_model.approve_legitimate
        fraudulent_cost = cost_model.approve_fraudulent

    elif action == Action.HOLD:
        legitimate_cost = cost_model.hold_legitimate
        fraudulent_cost = cost_model.hold_fraudulent

    else:
        legitimate_cost = cost_model.stop_legitimate
        fraudulent_cost = cost_model.stop_fraudulent

    return (
        belief.legitimate_probability * legitimate_cost
        + belief.fraudulent_probability * fraudulent_cost
    )


def make_decision(
    belief: Belief,
    cost_model: CostModel = DEFAULT_COST_MODEL,
) -> Decision:
    expected_costs = {}

    for action in Action:
        expected_costs[action] = calculate_expected_cost(
            belief,
            action,
            cost_model,
        )

    chosen_action = min(
        expected_costs,
        key=expected_costs.get,
    )

    return Decision(
        action=chosen_action,
        expected_cost=expected_costs[chosen_action],
    )