# Research Notes — Transaction Agent

## 1. Problem Statement

A financial transaction arrives with incomplete information. The agent must decide whether to approve, question/hold, or stop the transaction because the true legitimacy of the transaction is not directly known.

---

## 2. Project Objective

The objective is to explore how an agent can make decisions under uncertainty using:

- Probability
- New evidence
- Belief updates
- Decision thresholds
- Costs associated with different outcomes

The project is intentionally kept small so that the reasoning behind the agent can be understood and tested.

---

## 3. Agent Overview

The Transaction Agent receives information about a transaction and estimates the probability that it is legitimate or fraudulent.

The basic process is:

Transaction
↓
Observe available evidence
↓
Estimate belief about hidden state
↓
Receive new evidence
↓
Update belief
↓
Consider decision costs
↓
Choose an action

---

## 4. Hidden State

For the initial model, the hidden state has two possibilities:

- Legitimate
- Fraudulent

The agent does not directly observe the true state when making the initial decision.

---

## 5. Observable Information

The initial model considers:

- Transaction amount
- Transaction time
- Merchant history
- Recent transaction activity

These are the information available to the agent when evaluating a transaction.

---

## 6. Possible Actions

The agent can take three actions:

### Approve

Allow the transaction to proceed.

### Question / Hold

Temporarily hold the transaction or request additional verification/evidence.

### Stop

Prevent the transaction from proceeding.

---

## 7. Probability Model

The agent starts with a prior belief about the hidden state.

For the initial simulation, we use:

- Legitimate: 90%
- Fraudulent: 10%

These values represent an initial model assumption.

When new evidence is observed, the agent updates its belief about the hidden state.

The core probability process is:

**Prior → New Evidence → Posterior**

The posterior probability is then used by the decision policy to select an action.

---

## 8. Decision Costs

The three possible actions can produce different consequences depending on the actual hidden state.

| Action | Actual State | Outcome |
|---|---|---|
| Approve | Legitimate | Successful transaction |
| Approve | Fraudulent | Potential financial loss |
| Stop | Fraudulent | Fraud prevented |
| Stop | Legitimate | Customer inconvenience |
| Question / Hold | Legitimate | Verification delay |
| Question / Hold | Fraudulent | Additional investigation |

Therefore, the agent should not consider probability alone.

It should also consider the cost of making an incorrect decision.

---

## 9. Decision Process

The agent follows this general reasoning process:

1. A transaction arrives.
2. The agent observes available transaction information.
3. The agent starts with a prior belief.
4. New evidence changes the belief.
5. The agent obtains an updated probability.
6. The updated probability is compared with the decision policy.
7. The agent chooses:
   - Approve
   - Question / Hold
   - Stop
8. The eventual outcome can provide information for evaluating the decision.

---

## 10. Core Questions

The project is built around understanding:

- What information can the agent observe?
- What information remains hidden?
- How should new evidence change the agent's belief?
- How should probability affect the action?
- How should the cost of mistakes affect the decision?
- When should the agent request additional information instead of making a final decision?
- How should the agent's decisions be evaluated?

---

## 11. Technical Concepts

The project currently uses or investigates these concepts:

- Probability
- Conditional probability
- Prior probability
- Likelihood
- Posterior probability
- Bayesian updating
- Decision threshold
- Expected cost
- False positive
- False negative
- Human-in-the-loop
- Transaction monitoring
- Transaction velocity
- Fraud risk

---

ons when the true state is uncertain.

