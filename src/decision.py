from transaction_agent import Action, Belief, CostModel, Decision

DEFAULT_COST_MODEL = CostModel(
    approve_legitimate=0.0,
    approve_fraudulent=10.0,
    hold_legitimate=2.0,
    hold_fraudulent=2.0,
    stop_legitimate=8.0,
    stop_fraudulent=0.0,
)


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